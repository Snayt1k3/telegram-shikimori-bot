from typing import Optional

from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.adapters.database.common.db import Base
from src.adapters.database.sql.title.orm import Title
from src.domain.user import UserEntity, ShikiCredsEntity, UserRateEntity


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

    def to_entity(self):
        return ShikiCredsEntity(
            id=self.id,
            access=self.access,
            refresh=self.refresh,
            expire_in=self.expire_in
        )


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

    user_rates: Mapped[list["UserRate"]] = relationship(
        "UserRate", back_populates="user", collection_class=list
    )
    """Список оценок пользователя"""

    creds: Mapped[ShikiCredential] = relationship("ShikiCredential", foreign_keys=[cred_id])
    """Данные авторизации на shikimori.one"""

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            id_telegram=self.id_telegram,
            nickname=self.nickname,
            avatar=self.avatar,
            allow_notifications=self.allow_notifications,
            creds=self.creds.to_entity(),
            user_rates=[u.to_entity() for u in self.user_rates]
        )

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

    user: Mapped[User] = relationship("User", back_populates="user_rates")
    """Пользователь, которому принадлежит оценка"""

    title: Mapped[Title] = relationship("Title", foreign_keys=[title_id])

    def to_entity(self) -> UserRateEntity:
        return UserRateEntity()