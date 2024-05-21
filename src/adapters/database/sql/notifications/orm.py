from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from src.adapters.database.common.db import Base


class AnilibriaAnimeModel(Base):
    __tablename__ = 'anilibria_animes'
    id = Column(Integer, primary_key=True, index=True)
    ru = Column(String)
    en = Column(String)
    episode = Column(Integer)
    created_at = Column(DateTime)

class NotificationModel(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    anilibria_anime_id = Column(Integer, ForeignKey('anilibria_animes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_sended = Column(Boolean, default=False)

