from dataclasses import asdict

from anilibria import AniLibriaClient

from src.application.dto.user.follows import FollowListDTO, FollowDTO
from src.application.interfaces import AbstractCache, UseCase, AbstractUnitOfWork
from src.domain.user import UserEntity


class AddFollowUseCase(UseCase):
    """
    add follow on anime
    """

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def __call__(self, id_telegram: int, anime_id: int):
        async with self.uow as uow:
            user: UserEntity = await uow.user.find_one(id_telegram=id_telegram)

            user.add_follow(anime_id)
            await uow.user.edit_one(user)
            await uow.commit()


class DeleteFollowUseCase(UseCase):
    """
    deleting follow on anime
    """

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def __call__(self, id_telegram: int, anime_id: int):
        async with self.uow as uow:
            user: UserEntity = await uow.user.find_one(id_telegram=id_telegram)

            user.remove_follow(anime_id)
            await uow.user.edit_one(user)
            await uow.commit()


class GetAllFollowsUseCase(UseCase):
    """
    getting a user and return follow list
    """

    def __init__(
        self, anilibria: AniLibriaClient, uow: AbstractUnitOfWork, cache: AbstractCache
    ):
        self.cache = cache
        self.anilibria = anilibria
        self.uow = uow

    async def __call__(self, id_telegram: int) -> FollowListDTO:

        if data := await self.cache.get(f"{id_telegram}_follows"):
            return FollowListDTO.from_dict(data)

        async with self.uow as uow:
            user: UserEntity = await uow.user.find_one(id_telegram=id_telegram)

        titles = await self.anilibria.get_titles(user.follows)

        follow_objs = [
            FollowDTO(
                id=title.id,
                en=title.names.en,
                ru=title.names.ru,
                status=title.status.string,
            )
            for title in titles.list
        ]

        follow_list = FollowListDTO(follows=follow_objs)

        await self.cache.set(
            f"{id_telegram}_follows", asdict(follow_list), expire_in=60 * 60 * 4
        )

        return follow_list
