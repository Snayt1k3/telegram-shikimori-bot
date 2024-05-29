from anilibria import AniLibriaClient

from src.application.common.constants import ANILIBRIA_URL
from src.application.dto.title.torrent import TorrentDTO
from src.application.interfaces.usecases import UseCase


class GetTorrentUseCase(UseCase):
    """
    get a torrent urls for anilibria title
    """

    def __init__(self, anilibria: AniLibriaClient):
        self.anilibria = anilibria

    async def __call__(self, id: int) -> list[TorrentDTO]:
        title = await self.anilibria.get_title(id=id)
        return [
            TorrentDTO(
                episodes=tor.episodes.string,
                size=tor.total_size,
                url=ANILIBRIA_URL + tor.url,
                quality=tor.quality.string,
            )
            for tor in title.torrents.list
        ]
