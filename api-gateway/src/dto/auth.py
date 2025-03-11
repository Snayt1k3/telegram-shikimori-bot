from pydantic import BaseModel


class UserCheckDTO(BaseModel):
    telegram_id: int


class UserAuthDTO(BaseModel):
    telegram_id: int
    token: str


class User(BaseModel):
    id: int
    shikimori_id: int
    token: str
