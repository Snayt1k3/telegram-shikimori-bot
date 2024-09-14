import logging
from dataclasses import asdict

from shikimori.exceptions import RequestError
from shikimori.client import Shikimori

from src.application.exceptions.base import UnexpectedError
from src.application.exceptions.user import Unauthorised
from src.application.dto.user.auth import ShikiCredsDTO
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.user import ShikiCredsEntity

logger = logging.getLogger(__name__)


class GetURIUseCase(UseCase):
    """
    Sending uri to user.
    uri - url to get authorization code for access user account
    """

    def __init__(self, shiki: Shikimori):
        self.shiki = shiki

    async def __call__(self) -> str:
        return self.shiki.auth.auth_url


class GetCredentialsUseCase(UseCase):
    """
    Get JWT tokens from db, if tokens is expired they will be updated them.
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def _update_creds(self, creds: ShikiCredsEntity):
        new_creds = await self.shiki.auth.refresh(creds.refresh)

        if isinstance(new_creds, RequestError):
            if new_creds.status_code == 403:
                raise Unauthorised(f"Error with user credentials - {str(new_creds)}")

            raise UnexpectedError(
                f"Error occurred while requesting to shikimori.api - {str(new_creds)}"
            )

        creds.update_creds(
            new_creds.access_token,
            new_creds.refresh_token,
            new_creds.created_at,
        )

        return await self.uow.shiki_creds.edit_one(creds)

    async def __call__(self, id_telegram: int) -> ShikiCredsDTO:
        async with self.uow:
            user = await self.uow.user.find_one(id_telegram=id_telegram)

            if user.creds.is_expired():
                creds = await self._update_creds(user.creds)
                await self.uow.commit()

            else:
                creds = user.creds

        return ShikiCredsDTO.from_dict(asdict(creds))
