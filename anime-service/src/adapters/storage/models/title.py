from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.storage.models.base import Base


class TitleModel(Base):
    __tablename__ = "titles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    mal_id: Mapped[int] = mapped_column(index=True)
    title_ru: Mapped[str] = mapped_column(String)
    title_en: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, index=True)
    score: Mapped[str] = mapped_column(String)
    episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    episodes_aired: Mapped[int] = mapped_column(Integer, nullable=True)
    volumes: Mapped[int] = mapped_column(Integer, nullable=True)
    chapters: Mapped[int] = mapped_column(Integer, nullable=True)
