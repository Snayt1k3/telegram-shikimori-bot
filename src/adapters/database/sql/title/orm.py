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

    episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    """Количество эпизодов"""

    episodes_aired: Mapped[int] = mapped_column(Integer, nullable=True)
    """Количество вышедших эпизодов"""

    volumes: Mapped[int] = mapped_column(Integer, nullable=True)
    """Количество томов"""

    chapters: Mapped[int] = mapped_column(Integer, nullable=True)
    """Количество глав"""

    def to_entity(self) -> TitleEntity:
        return TitleEntity(
            title_en=self.title_en,
            title_ru=self.title_ru,
            chapters=self.chapters,
            volumes=self.volumes,
            status=self.status,
            score=self.score,
            id=self.id,
            image_url=self.image_url,
            episodes=self.episodes,
            episodes_aired=self.episodes_aired,
        )
