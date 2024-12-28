from shikimori import Shikimori
from src.dto.auth import CheckData, AuthData
from src.adapters.uow import AbstractUow
from src.dto.response import ResponseDTO


class CheckUserHandler:
    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self.uow = uow
        self.shiki = shiki

    async def __call__(self, data: CheckData) -> ResponseDTO:
        pass


class GetUriHandler:
    def __init__(self, shiki: Shikimori):
        self.shiki = shiki

    async def __call__(self) -> ResponseDTO:
        pass


class AuthUserHandler:
    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self.uow = uow
        self.shiki = shiki

    async def __call__(self, data: AuthData) -> ResponseDTO:
        pass
