from contextlib import asynccontextmanager
from typing import AsyncContextManager

from shikimori import Shikimori

from src.adapters.uow import SqlAlchemyUnitOfWork
from src.adapters.storage.base import get_session
from src.handlers import CheckUserHandler, GetUriHandler, AuthUserHandler
from src.config.shiki import shiki_cfg


class IoC:
    """dependency container"""

    @asynccontextmanager
    async def check_user(self) -> AsyncContextManager[CheckUserHandler]:
        uow = SqlAlchemyUnitOfWork(get_session())
        shiki = Shikimori(
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
        )
        yield CheckUserHandler(uow, shiki)

    @asynccontextmanager
    async def auth_user(self) -> AsyncContextManager[AuthUserHandler]:
        uow = SqlAlchemyUnitOfWork(get_session())
        shiki = Shikimori(
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
        )
        yield AuthUserHandler(uow, shiki)

    @asynccontextmanager
    async def get_uri(self) -> AsyncContextManager[GetUriHandler]:
        shiki = Shikimori(
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
        )
        yield GetUriHandler(shiki)
