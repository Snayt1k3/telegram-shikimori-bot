from typing import List

from pydantic import BaseModel

from database.schemas.base import Base


class AnimeBase(BaseModel):
    title_ru: str = ""
    title_en: str = ""
    id: int = None


class ShikimoriAnime(AnimeBase):
    pass


class AnilibriaAnime(AnimeBase):
    pass
