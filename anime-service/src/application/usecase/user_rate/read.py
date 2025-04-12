from src.adapters.storage.models.user_rate import UserRateModel
from src.application.interfaces import AbstractUow, UseCase
from src.application.dto import RatesGet


class ReadManyRates(UseCase):
    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RatesGet) -> list[UserRateModel]:
        filters = {}

        if data.get("status") is not None:
            filters["status"] = data["status"]

        if data.get("user_id") is not None:
            filters["user_id"] = data["user_id"]

        if data.get("ids") is not None:
            filters["id__in"] = data["ids"]

        async with self.uow as uow:
            return await uow.user_rate.find_many(**filters)
