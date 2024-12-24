from pydantic import BaseModel


class UserAuthDTO(BaseModel):
    id: str
