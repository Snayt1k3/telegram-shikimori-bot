from dataclasses import asdict

from anilibria import AniLibriaClient

from src.application.dto.title.search import SearchResultDTO
from src.application.interfaces import AbstractCache, UseCase


class AnilibriaGetTitleUseCase(UseCase):

    def __init__(self, anilibria: AniLibriaClient, cache: AbstractCache):
        self.cache = cache
        self.anilibria = anilibria

    async def __call__(self, id: int) -> SearchResultDTO:

        if data := await self.cache.get(f"anilibria_{id}"):
            return SearchResultDTO.from_dict(data)

        title = await self.anilibria.get_title(id)
        res = SearchResultDTO(
            title.id,
            title.names.ru,
            title.names.en,
            title.posters.small.full_url,
            title.status.string,
            {"voicers": title.team.voice},
        )

        await self.cache.set(f"anilibria_{id}", asdict(res), expire_in=60 * 60 * 24)

        return res
