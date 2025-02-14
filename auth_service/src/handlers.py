from datetime import datetime, timedelta
from shikimori import Shikimori
from shikimori.exceptions import RequestError
from fastapi import HTTPException
from src.adapters.storage.models import User
from src.adapters.uow import AbstractUow
from src.dto.auth import CheckData, AuthData
from src.dto.response import ResponseDTO


class CheckUserHandler:
    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self.uow = uow
        self.shiki = shiki

    async def __call__(self, data: CheckData) -> ResponseDTO:
        async with self.uow as uow:
            user: User = await uow.user.find_one(id=data.user_id)

            if user is None:
                raise HTTPException(detail="User not found.", status_code=404)

            now = datetime.now()

            if user.expired_at <= now or (user.expired_at - now).total_seconds() <= 600:
                new_token = await self.shiki.auth.refresh(user.refresh_token)

                if isinstance(new_token, RequestError):
                    raise HTTPException(
                        detail="Failed to refresh token.", status_code=401
                    )

                await uow.user.update_one(
                    id=data.user_id,
                    token=new_token.access_token,
                    refresh_token=new_token.refresh_token,
                    expired_at=datetime.now() + timedelta(hours=24),
                )
                user.token = new_token.access_token

            return ResponseDTO(
                data={
                    "id": data.user_id,
                    "shikimori_id": user.shikimori_id,
                    "token": user.token,
                },
                error=None,
                status=200,
            )


class GetUriHandler:
    def __init__(self, shiki: Shikimori):
        self.shiki = shiki

    async def __call__(self) -> ResponseDTO:
        return ResponseDTO(
            data={"uri": self.shiki.auth.auth_url}, error=None, status=200
        )


class AuthUserHandler:
    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self.uow = uow
        self.shiki = shiki

    async def __call__(self, data: AuthData) -> ResponseDTO:
        auth_data = await self.shiki.auth.get_access_token(data.token)

        if isinstance(auth_data, RequestError):
            raise HTTPException(detail=str(auth_data), status_code=400)

        self.shiki.set_token(auth_data.access_token)
        user = await self.shiki.user.whoami()

        async with self.uow as uow:
            user = await uow.user.add_one(
                id=data.user_id,
                token=auth_data.access_token,
                refresh_token=auth_data.refresh_token,
                expired_at=datetime.now() + timedelta(hours=24),
                shikimori_id=user.id,
            )

            return ResponseDTO(
                status=200,
                error=None,
                data={
                    "id": user.id,
                    "token": user.token,
                    "shikimori_id": user.shikimori_id,
                },
            )
