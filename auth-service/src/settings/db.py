from pydantic import Field

from src.settings.base import Settings


class DBSettings(Settings):
    AUTH_POSTGRES_USER: str = Field()
    AUTH_POSTGRES_PASSWORD: str = Field()
    AUTH_POSTGRES_DB: str = Field()
    AUTH_POSTGRES_HOST: str = Field()

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.AUTH_POSTGRES_USER}:{self.AUTH_POSTGRES_PASSWORD}@{self.AUTH_POSTGRES_HOST}:5432/{self.AUTH_POSTGRES_DB}"


db_settings = DBSettings()
