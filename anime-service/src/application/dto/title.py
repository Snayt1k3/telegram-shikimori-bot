from typing import TypedDict


class TitlesGET(TypedDict):
    title_ru: str
    title_en: str
    score: str
    status: str
    ids: list[int]
