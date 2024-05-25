from shikimori.client import Shikimori

from src.application.dto.user.auth import ShikiCredsDTO
from src.application.dto.user.user import UserDTO
from src.application.dto.user.user import (
    UserUpdateDTO,
)
from src.application.interfaces.database.uow.base import AbstractUnitOfWork
from src.application.interfaces.usecases.base import UseCase


class AddUserUseCase(UseCase):
    """
    add a new user
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, code: str, id_telegram: int) -> UserDTO:
        creds = await self.shiki.auth.get_access_token(code)

        self.shiki.set_token(creds.access_token)
        user = await self.shiki.user.whoami()

        async with self.uow:
            creds_id = await self.uow.shiki_creds.add_one(
                {
                    "access": creds.access_token,
                    "refresh": creds.refresh_token,
                    "expire_in": creds.expires_in,
                }
            )

            user_id = await self.uow.user.add_one(
                {
                    "nickname": user.nickname,
                    "cred_id": creds_id,
                    "id_telegram": id_telegram,
                    "avatar": user.avatar_url,
                }
            )
            await self.uow.commit()
            user = await self.uow.user.find_one(id=user_id)

        return UserDTO(
            id=user.id,
            id_telegram=user.id_telegram,
            nickname=user.nickname,
            avatar=user.avatar,
            user_rates=user.user_rates,
            creds=ShikiCredsDTO(
                id=user.creds.id,
                access=user.creds.access_token,
                refresh=user.creds.refresh_token,
                expire_in=user.creds.expires_in)
        )
class DeleteUserUseCase(UseCase):
    """
    delete user from db
    """

    def __call__(self, id: int):
        pass

class UpdateUserUseCase(UseCase):
    """
    updating user in db
    """
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, obj: UserUpdateDTO):
        pass
