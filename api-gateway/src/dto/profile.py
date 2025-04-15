from pydantic import BaseModel


class UserProfileDTO(BaseModel):
    username: str
    avatar: str
    animes: dict[str, int]
    mangas: dict[str, int]
