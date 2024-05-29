import datetime
from dataclasses import asdict

from shikimori.client import Shikimori

from src.application.dto.user.user import UserDTO
from src.application.dto.user.user import (
    UserUpdateDTO,
)
from src.application.interfaces.database.uow import AbstractUnitOfWork
from src.application.interfaces.usecases import UseCase
from src.domain.user import ShikiCredsEntity


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
            shiki_db: ShikiCredsEntity = await self.uow.shiki_creds.add_one(
                {
                    "access": creds.access_token,
                    "refresh": creds.refresh_token,
                    "expire_in": datetime.datetime.fromtimestamp(creds.created_at)
                    + datetime.timedelta(days=1),
                }
            )

            new_user = await self.uow.user.add_one(
                {
                    "nickname": user.nickname,
                    "cred_id": shiki_db.id,
                    "id_telegram": id_telegram,
                    "avatar": user.avatar_url,
                }
            )
            await self.uow.commit()

        return UserDTO.from_dict(asdict(new_user))


class DeleteUserUseCase(UseCase):
    """
    delete user from db
    """

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def __call__(self, id_telegram: int) -> UserDTO:
        async with self.uow:
            user = await self.uow.user.find_one(id_telegram=id_telegram)
            user = await self.uow.user.delete_one(user.id)
            await self.uow.commit()
        return UserDTO.from_dict(asdict(user))


class UpdateUserUseCase(UseCase):
    """
    updating user in db
    """

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def __call__(self, obj: UserUpdateDTO, id_telegram: int) -> None:
        async with self.uow:
            user = await self.uow.user.find_one(id_telegram=id_telegram)
            user.update_user(obj)
            await self.uow.user.edit_one(user.id, asdict(obj))
            await self.uow.commit()
