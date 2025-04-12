from src.adapters.storage.models.title import TitleModel
from src.application.dto import TitlesGET
from src.application.interfaces import AbstractUow, UseCase


class ReadManyTitles(UseCase):
    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: TitlesGET) -> list[TitleModel]:
        filters = {}

        if data.get("title_ru") is not None:
            filters["title_ru__icontains"] = data["title_ru"]

        if data.get("title_en") is not None:
            filters["title_en__icontains"] = data["title_en"]

        if data.get("score") is not None:
            filters["score"] = data["score"]

        if data.get("status") is not None:
            filters["status"] = data["status"]

        if data.get("ids") is not None:
            filters["id__in"] = data["ids"]

        async with self.uow as uow:
            return await uow.title.find_many()
