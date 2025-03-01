from pydantic import Field
from src.config.base import BaseConfig


class DatabaseConfig(BaseConfig):
    ANIME_POSTGRES_USER: str = Field()
    ANIME_POSTGRES_PASSWORD: str = Field()
    ANIME_POSTGRES_DB: str = Field()
    ANIME_POSTGRES_HOST: str = Field()
    ANIME_POSTGRES_PORT: str = Field()

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.ANIME_POSTGRES_USER}:{self.ANIME_POSTGRES_PASSWORD}@{self.ANIME_POSTGRES_HOST}:{self.ANIME_POSTGRES_PORT}/{self.ANIME_POSTGRES_DB}"


db_config = DatabaseConfig()
