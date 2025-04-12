from src.adapters.storage.models.user_rate import UserRateModel
from src.application.dto import RatesUpdate
from src.application.interfaces import AbstractUow, UseCase
from src.tasks.sync import start_sync_user_rate


class UpdateRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RatesUpdate) -> UserRateModel:
        async with self.uow as uow:
            res: UserRateModel = await uow.user_rate.update_one(
                **{k: v for k, v in data if v is not None}
            )

        start_sync_user_rate(res.id)

        return res
