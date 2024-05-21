from sqlalchemy import Integer, Column, Boolean, ForeignKey, Table
from sqlalchemy import String

from src.adapters.database.common.db import mapper_registry


shiki_credentials = Table(
    "shiki_credentials",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("access", String),
    Column("refresh", String),
    Column("expire_in", String),
)

# Определяем таблицу users
users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("id_telegram", Integer, index=True),
    Column("nickname", String, index=True),
    Column("cred_id", Integer, ForeignKey("shiki_credentials.id")),
    Column("avatar", String),
    Column("allow_notifications", Boolean, default=True),
)
