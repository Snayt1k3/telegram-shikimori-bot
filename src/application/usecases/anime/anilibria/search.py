from dataclasses import asdict

from anilibria import AniLibriaClient

from src.application.dto.title.search import SearchResultsDTO, SearchResultDTO
from src.application.interfaces.cache import AbstractCache
from src.application.interfaces.usecases import UseCase


class AnilibriaSearchUseCase(UseCase):
    """
    Searching Anime via anilibria api
    """

    def __init__(self, anilibria: AniLibriaClient, cache: AbstractCache):
        self.cache = cache
        self.anilibria = anilibria

    async def __call__(self, query: str) -> SearchResultsDTO:

        if data := await self.cache.get(query):
            return SearchResultsDTO.from_dict(data)

        titles = await self.anilibria.search_titles([query])
        results = [
            SearchResultDTO(
                title.id,
                title.names.ru,
                title.names.en,
                title.posters.small.full_url,
                title.status.string,
                {"voicers": title.team.voice},
            )
            for title in titles.list
        ]
        res = SearchResultsDTO(query, results)

        await self.cache.set(query + "anilibria", asdict(res), expire_in=60 * 60 * 24)

        return res
