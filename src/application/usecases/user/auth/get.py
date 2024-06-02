from dataclasses import asdict

from shikimori.client import Shikimori

from src.application.dto.user.auth import ShikiCredsDTO
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.user import ShikiCredsEntity


class GetURIUseCase(UseCase):
    def __init__(self, shiki: Shikimori):
        self.shiki = shiki

    async def __call__(self) -> str:
        return self.shiki.auth.auth_url


class GetCredentialsUseCase(UseCase):
    """
    getting credentials from db, if creds is expired, they will update
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def _update_creds(self, creds: ShikiCredsEntity):
        new_creds = await self.shiki.auth.refresh(creds.refresh)

        creds.update_creds(
            new_creds.access_token,
            new_creds.refresh_token,
            new_creds.created_at,
        )
        return self.uow.shiki_creds.edit_one(creds)

    async def __call__(self, id_telegram: int) -> ShikiCredsDTO:
        async with self.uow:
            user = await self.uow.user.find_one(id_telegram=id_telegram)

            if user.creds.is_expired():
                creds = await self._update_creds(user.creds)
                await self.uow.commit()

            else:
                creds = user.creds

        return ShikiCredsDTO.from_dict(asdict(creds))