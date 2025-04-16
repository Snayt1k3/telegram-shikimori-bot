import datetime
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.storage.models.base import Base
from src.adapters.storage.models.title import TitleModel


class UserRateModel(Base):
    __tablename__ = "user_rates"

    user_id: Mapped[int] = mapped_column(Integer)
    title_id: Mapped[int] = mapped_column(Integer, ForeignKey("titles.id"))
    target_type: Mapped[str] = mapped_column(String, index=True)
    score: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)
    episodes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chapters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    volumes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rewatches: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    title: Mapped[TitleModel] = relationship(
        "Title", foreign_keys=[title_id], lazy="joined"
    )
