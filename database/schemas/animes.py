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


class ShikimoriAnimeList(Base):
    animes: List[ShikimoriAnime]


class AnilibriaAnimeList(Base):
    animes: List[AnilibriaAnime]
