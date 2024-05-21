from sqlalchemy import Integer, Column, Boolean, ForeignKey
from sqlalchemy import String

from src.adapters.database.common.db import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    id_telegram = Column(Integer, index=True)
    nickname = Column(String, index=True)
    cred_id = Column(Integer, ForeignKey('shiki_credentials.id'))
    avatar = Column(String)
    allow_notifications = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return ""


class ShikiCredentialModel(Base):
    __tablename__ = 'shiki_credentials'
    id = Column(Integer, primary_key=True, index=True)
    access = Column(String)
    refresh = Column(String)
    expire_in = Column(String)

    def __repr__(self) -> str:
        return ""
