from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.user_rate import UserRateEntity
from src.adapters.database.common.db import Base


class UserRate(Base):
    __tablename__ = "user_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    """Идентификатор пользователя"""

    title_id: Mapped[int] = mapped_column(Integer, ForeignKey("titles.id"))
    """Идентификатор тайтла"""

    target_id: Mapped[int] = mapped_column(Integer, index=True)
    """Идентификатор цели"""

    target_type: Mapped[str] = mapped_column(String, index=True)
    """Тип цели"""

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

    def to_entity(self) -> UserRateEntity:
        return UserRateEntity()
