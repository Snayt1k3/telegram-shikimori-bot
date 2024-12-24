from pydantic import BaseModel


class AuthDTO(BaseModel):
    id: str
