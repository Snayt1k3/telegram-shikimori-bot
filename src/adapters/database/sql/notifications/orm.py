from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Boolean,
    TIMESTAMP,
)
from sqlalchemy.orm import mapped_column, Mapped

from src.adapters.database.common.db import Base
from src.domain.notifications import AnimeAL, NotificationEntity


class AnilibriaAnime(Base):
    __tablename__ = "anilibria_animes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    ru: Mapped[str] = mapped_column(String)
    """Название на русском языке"""

    en: Mapped[str] = mapped_column(String)
    """Название на английском языке"""

    episode: Mapped[int] = mapped_column(Integer)
    """Количество эпизодов"""

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    """Дата создания записи"""

    def to_entity(self) -> AnimeAL:
        return AnimeAL()


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    anilibria_anime_id: Mapped[int] = mapped_column(ForeignKey("anilibria_animes.id"))
    """Идентификатор аниме в базе Anilibria"""

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    """Идентификатор пользователя"""

    is_sended: Mapped[bool] = mapped_column(Boolean, default=False)
    """Статус отправки уведомления"""


    def to_entity(self) -> NotificationEntity:
        return NotificationEntity()
