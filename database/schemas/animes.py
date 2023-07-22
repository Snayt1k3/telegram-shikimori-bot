from pydantic import BaseModel
from typing import List
from database.schemas.base import Base


class AnimeBase(BaseModel):
    title_ru: str = ''
    title_en: str = ''
    id: int = None


class ShikimoriAnime(AnimeBase):
    pass


class AnilibriaAnime(AnimeBase):
    pass


class AnimeSearch(Base):
    animes: List[ShikimoriAnime] | List[AnilibriaAnime] = None
    phrase: str = ''
