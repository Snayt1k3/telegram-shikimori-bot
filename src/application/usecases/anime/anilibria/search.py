from anilibria import AniLibriaClient

from src.application.dto.title.search import SearchResultsDTO, SearchResultDTO
from src.application.interfaces.usecases import UseCase


class AnilibriaSearchUseCase(UseCase):
    """
    Searching Anime via anilibria api
    """

    def __init__(self, anilibria: AniLibriaClient, cache: "AbstractCache"):
        self.cache = cache
        self.anilibria = anilibria

    async def __call__(self, query: str) -> SearchResultsDTO:

        # TODO получение данных из cache

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

        # TODO здесь сохранение в cache

        return res