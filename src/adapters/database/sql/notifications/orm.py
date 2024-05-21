from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Table,
    TIMESTAMP,
)

from src.adapters.database.common.db import mapper_registry

AnilibriaAnimeModel = Table(
    "AnilibriaAnimeModel",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("ru", String),
    Column("en", String),
    Column("episode", Integer),
    Column("created_at", TIMESTAMP(timezone=True), default=datetime.utcnow()),
)


notifications = Table(
    "notifications",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("anilibria_anime_id", Integer, ForeignKey('anilibria_animes.id')),
    Column("user_id", Integer, ForeignKey('users.id')),
    Column("is_sended", Boolean, default=False),
)

def notifications_mapper():
    raise NotImplementedError
