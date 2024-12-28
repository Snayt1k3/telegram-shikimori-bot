from contextlib import asynccontextmanager

from src.dto.response import ResponseDTO


class IoC:

    @asynccontextmanager
    async def check_user(self) -> ResponseDTO:
        pass

    @asynccontextmanager
    async def auth_user(self) -> ResponseDTO:
        pass

    @asynccontextmanager
    async def get_uri(self) -> ResponseDTO:
        pass
