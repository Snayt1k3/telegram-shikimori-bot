import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.storage.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shikimori_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    expired_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
