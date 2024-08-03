from .info import router as info_router
from .lists import router as lists_router
from .edit import router as edit_router
from .episode import router as episode_router
from .user_rate import router as user_rate_router


__all__ = [
    "info_router",
    "lists_router",
    "edit_router",
    "episode_router",
    "user_rate_router",
]
