from pydantic import BaseModel


class AuthData(BaseModel):
    token: str
    user_id: int


class CheckData(BaseModel):
    user_id: int
