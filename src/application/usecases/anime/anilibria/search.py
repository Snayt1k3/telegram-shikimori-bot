from anilibria import AniLibriaClient

from src.application.dto.title.search import SearchResults, SearchResult
from src.application.interfaces.usecases.base import UseCase


class AnilibriaSearchUseCase(UseCase):
    """
    Searching Anime via anilibria api
    """

    def __init__(self, anilibria: AniLibriaClient, cache: "AbstractCache"):
        self.cache = cache
        self.anilibria = anilibria

    async def __call__(self, query: str) -> SearchResults:

        # TODO получение данных из cache

        titles = await self.anilibria.search_titles([query])
        results = [
            SearchResult(
                title.id,
                title.names.ru,
                title.names.en,
                title.posters.small.full_url,
                title.status.string,
                {"voicers": title.team.voice},
            )
            for title in titles.list
        ]
        res = SearchResults(query, results)

        # TODO здесь сохранение в cache

        return res