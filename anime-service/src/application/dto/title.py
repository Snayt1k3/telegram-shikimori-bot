from typing import TypedDict


class TitlesGET(TypedDict):
    title_ru: str | None
    title_en: str | None
    score: str | None
    status: str | None
    ids: list[int] | None
