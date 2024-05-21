from sqlalchemy import Integer, Column, Boolean, ForeignKey, Table
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from src.adapters.database.common.db import Base
from src.domain.user import UserEntity


class ShikiCredential(Base):
    __tablename__ = "shiki_credentials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    access: Mapped[str] = mapped_column(String)
    """Access-токен"""

    refresh: Mapped[str] = mapped_column(String)
    """Refresh-токен"""

    expire_in: Mapped[str] = mapped_column(String)
    """Срок действия токена"""


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Идентификатор в бд"""

    id_telegram: Mapped[int] = mapped_column(Integer, index=True)
    """Идентификатор в Telegram"""

    nickname: Mapped[str] = mapped_column(String, index=True)
    """Никнейм пользователя"""

    cred_id: Mapped[int] = mapped_column(Integer, ForeignKey("shiki_credentials.id"))
    """Идентификатор учётных данных Shiki"""

    avatar: Mapped[str] = mapped_column(String)
    """URL аватара пользователя"""

    allow_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    """Разрешение на получение уведомлений"""

    def to_entity(self) -> UserEntity:
        return UserEntity()
