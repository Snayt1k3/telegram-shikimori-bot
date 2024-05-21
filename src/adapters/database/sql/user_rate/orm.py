from sqlalchemy import ForeignKey, Integer, Column, Table
from sqlalchemy import String

from src.adapters.database.common.db import mapper_registry


user_rates = Table(
    "user_rates",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("title_id", Integer, ForeignKey("titles.id")),
    Column("target_id", Integer, index=True),
    Column("target_type", String, index=True),
    Column("score", Integer),
    Column("status", String),
    Column("episodes", Integer, nullable=True),
    Column("chapters", Integer, nullable=True),
    Column("volumes", Integer, nullable=True),
    Column("rewatches", Integer, nullable=True),
)
