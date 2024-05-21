from sqlalchemy import Column, Integer, String, Table

from src.adapters.database.common.db import mapper_registry


titles = Table(
    "titles",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, index=True),
    Column("title_ru", String, index=True),
    Column("title_en", String, index=True),
    Column("image_url", String),
    Column("status", String),
    Column("score", String),
    Column("episodes", Integer),
    Column("episodes_aired", Integer),
    Column("volumes", Integer),
    Column("chapters", Integer),
)
