from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class CreateManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, objs: list[dict]) -> list[int]:
        async with self.uow as uow:
            objs_ids = await uow.user_rate.add_many(objs)

        return objs_ids


class CreateRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(
        self,
        id: int,
        title_id: int,
        user_id: int,
        shikimori_id: int,
        target_id: int,
        target_type: str,
        status: str,
        score: int,
        episodes: int,
        rewatches: int,
        volumes: int,
        chapters: int,
    ) -> int:
        async with self.uow as uow:
            obj_id = await uow.user_rate.add_one(
                id=id,
                status=status,
                score=score,
                episodes=episodes,
                volumes=volumes,
                chapters=chapters,
                target_id=target_id,
                target_type=target_type,
                rewatches=rewatches,
                title_id=title_id,
                shikimori_id=shikimori_id,
                user_id=user_id,
            )

        return obj_id
