from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Boolean,
    TIMESTAMP,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.adapters.database.common.db import Base
from src.adapters.database.sql.user.orm import User


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    ru: Mapped[str] = mapped_column(String)
    """Название на русском языке"""

    en: Mapped[str] = mapped_column(String)
    """Название на английском языке"""

    episode: Mapped[int] = mapped_column(Integer)
    """Эпизод который вышел"""

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    """Идентификатор пользователя"""

    is_sended: Mapped[bool] = mapped_column(Boolean, default=False)
    """Статус отправки уведомления"""

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
