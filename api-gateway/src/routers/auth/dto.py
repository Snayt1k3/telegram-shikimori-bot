from pydantic import BaseModel


class UserCheckDTO(BaseModel):
    id: int


class UserAuthDTO(BaseModel):
    id: int
    token: str


class User(BaseModel):
    id: str
    shikimori_id: str
    token: str
