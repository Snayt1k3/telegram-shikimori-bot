from dataclasses import asdict

from src.application.dto.title.search import SearchResultsDTO, SearchResultDTO
from src.application.enums.shikimori import ShikimoriEntryType
from src.application.interfaces.cache import AbstractCache
from src.application.interfaces.usecases import UseCase
from shikimori import Shikimori


class ShikimoriSearchUseCase(UseCase):
    """
    Searching Anime via shikimori api
    """

    def __init__(self, shiki: Shikimori, cache: AbstractCache):
        self.cache = cache
        self.shiki = shiki

    async def __call__(
        self, query: str, entryType: ShikimoriEntryType
    ) -> SearchResultsDTO:

        if data := await self.cache.get(query):
            return SearchResultsDTO.from_dict(data)

        if str(entryType) == "Anime":
            titles = await self.shiki.anime.list(search=query, limit=50)
        else:
            titles = await self.shiki.manga.list(search=query, limit=50)

        results = []

        for title in titles:
            results.append(SearchResultDTO(
                id=title.id,
                ru=title.russian,
                en=title.name,
                img=title.image.original_url,
                status=title.status,
                additional_data={
                    "episodes": getattr(title, "episodes", None),
                    "volumes": getattr(title, "volumes", None),
                    "episodes_aired": getattr(title, "episodes_aired", None),
                    "chapters": getattr(title, "chapters", None),
                }
            ))

        res = SearchResultsDTO(
            query=query,
            results=results,
        )

        await self.cache.set(query, asdict(res), expire_in=60 * 60 * 24)

        return res
