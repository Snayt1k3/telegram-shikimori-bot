from aiogram import Router

from .anilibria import torrent_router, title_router
from .search import router as search_router
from .shikimori import (
    edit_router,
    lists_router,
    info_router,
    user_rate_router,
    episode_router,
)


def include_anime_routers(router: Router):
    router.include_routers(
        search_router,
        edit_router,
        lists_router,
        info_router,
        torrent_router,
        title_router,
        user_rate_router,
        episode_router,
    )
