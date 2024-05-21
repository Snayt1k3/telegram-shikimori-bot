from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.adapters.database.common.db import Base
from src.domain.title import TitleEntity


class Title(Base):
    __tablename__ = "titles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    title_ru: Mapped[str] = mapped_column(String, index=True)
    """Название на русском языке"""

    title_en: Mapped[str] = mapped_column(String, index=True)
    """Название на английском языке"""

    image_url: Mapped[str] = mapped_column(String)
    """URL изображения"""

    status: Mapped[str] = mapped_column(String)
    """Статус тайтла"""

    score: Mapped[str] = mapped_column(String)
    """Оценка тайтла"""

    episodes: Mapped[int] = mapped_column(Integer)
    """Количество эпизодов"""

    episodes_aired: Mapped[int] = mapped_column(Integer)
    """Количество вышедших эпизодов"""

    volumes: Mapped[int] = mapped_column(Integer)
    """Количество томов"""

    chapters: Mapped[int] = mapped_column(Integer)
    """Количество глав"""

    def to_entity(self) -> TitleEntity:
        return TitleEntity()