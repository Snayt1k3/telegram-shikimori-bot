from pydantic import BaseModel


class UserCheckDTO(BaseModel):
    id: int


class UserAuthDTO(BaseModel):
    id: int
    token: str


class User(BaseModel):
    id: int
    shikimori_id: int
    token: str
