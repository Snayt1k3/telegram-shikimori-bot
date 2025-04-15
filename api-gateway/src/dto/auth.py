from pydantic import BaseModel, Field


class UserGetRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram user ID", ge=1)


class UserAuthRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram user ID", ge=1)
    token: str = Field(..., description="Shikimori auth token")


class AuthenticatedUser(BaseModel):
    telegram_id: int
    shikimori_id: int
    token: str
