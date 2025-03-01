from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config.db import db_config

DATABASE_URL = db_config.url

engine = create_async_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
