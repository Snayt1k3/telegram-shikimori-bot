import datetime

from sqlalchemy import inspect, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from src.config.db import db_config

DATABASE_URL = db_config.url

engine = create_async_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        onupdate=datetime.datetime.now(datetime.UTC),
    )


async_session_factory = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session  # type: ignore
