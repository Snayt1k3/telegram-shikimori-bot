from aiogram import Router
from .search import router as search_router

def include_anime_routers(router: Router):
    router.include_routers(search_router)

