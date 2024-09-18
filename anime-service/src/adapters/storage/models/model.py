from typing import Optional

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Title(Base):
    __tablename__ = "titles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    """Идентификатор в бд и шикимори"""

    mal_id: Mapped[int] = mapped_column(index=True)

    title_ru: Mapped[str] = mapped_column(String)
    """Название на русском языке"""

    title_en: Mapped[str] = mapped_column(String)
    """Название на английском языке"""

    image_url: Mapped[str] = mapped_column(String)
    """URL изображения"""

    status: Mapped[str] = mapped_column(String, index=True)
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


class UserRate(Base):
    __tablename__ = "user_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    shikimori_id: Mapped[int] = mapped_column(Integer)
    """Идентификатор пользователя в системе Shikimori"""

    title_id: Mapped[int] = mapped_column(Integer, ForeignKey("titles.id"))
    """Идентификатор тайтла"""

    target_id: Mapped[int] = mapped_column(Integer, index=True)
    """Идентификатор цели"""

    target_type: Mapped[str] = mapped_column(String, index=True)
    """Тип Тайтла"""

    score: Mapped[int] = mapped_column(Integer)
    """Оценка"""

    status: Mapped[str] = mapped_column(String)
    """Статус"""

    episodes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Количество эпизодов"""

    chapters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Количество глав"""

    volumes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Количество томов"""

    rewatches: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Количество пересмотров"""

    title: Mapped[Title] = relationship("Title", foreign_keys=[title_id], lazy="joined")
