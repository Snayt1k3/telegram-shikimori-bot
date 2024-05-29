from src.application.dto.title.search import SearchResultsDTO, SearchResultDTO
from src.application.enums.shikimori import ShikimoriEntryType
from src.application.interfaces.usecases import UseCase
from shikimori import Shikimori


class ShikimoriSearchUseCase(UseCase):
    """
    Searching Anime via shikimori api
    """

    def __init__(self, shiki: Shikimori, cache: "AbstractCache"):  # todo add cache
        self.cache = cache
        self.shiki = shiki

    async def __call__(
        self, query: str, entryType: ShikimoriEntryType
    ) -> SearchResultsDTO:
        if str(entryType) == "Anime":
            titles = await self.shiki.anime.list(search=query, limit=50)
        else:
            titles = await self.shiki.manga.list(search=query, limit=50)

        results = []

        for title in titles:
            obj = SearchResultDTO(
                id=title.id,
                ru=title.russian,
                en=title.name,
                img=title.image.original_url,
                status=title.status,
                additional_data={} if str

            )
