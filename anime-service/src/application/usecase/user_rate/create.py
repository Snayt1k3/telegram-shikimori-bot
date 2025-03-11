from src.application.interfaces import AbstractUow, UseCase
from src.application.dto import RatesCreate


class CreateRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RatesCreate) -> int:
        # async with self.uow as uow:
        #     obj_id = await uow.user_rate.add_one(
        #         id=id,
        #         status=status,
        #         score=score,
        #         episodes=episodes,
        #         volumes=volumes,
        #         chapters=chapters,
        #         target_id=target_id,
        #         target_type=target_type,
        #         rewatches=rewatches,
        #         title_id=title_id,
        #         shikimori_id=shikimori_id,
        #         user_id=user_id,
        #     )
        #
        # return obj_id todo
        pass
