from src.dto.base import Model


class TitleFilterDTO(Model):
    title_ru: str = None
    title_en: str = None
    score: str = None
    status: str = None
    ids: list[int] = None
