from dataclasses import asdict

from shikimori.client import Shikimori

from src.application.dto.user.user import UserDTO
from src.application.dto.user.user import (
    UserUpdateDTO,
)
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.user import ShikiCredsEntity, UserEntity


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

        async with self.uow as uow:
            shiki_cred_id = await uow.shiki_creds.add_one(
                ShikiCredsEntity.create(
                    creds.access_token, creds.refresh_token, creds.created_at
                )
            )

            creds = await uow.shiki_creds.find_one(id=shiki_cred_id)

            new_user = await uow.user.add_one(
                UserEntity.create(
                    id=user.id,
                    nickname=user.nickname,
                    id_telegram=id_telegram,
                    avatar=user.avatar,
                    creds=creds,
                    user_rates=[],
                    follows=[],
                )
            )
            await self.uow.commit()

            new_user = await uow.user.find_one(id=new_user)

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
            await self.uow.user.edit_one(user)
            await self.uow.commit()
