from dotenv import load_dotenv
from pydantic import Field

from src.settings.base import Settings

load_dotenv()


class DBSettings(Settings):
    POSTGRES_USER: str = Field()
    POSTGRES_PASSWORD: str = Field()
    POSTGRES_DB: str = Field()
    POSTGRES_HOST: str = Field()
    POSTGRES_PORT: str = Field()

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


db_settings = DBSettings()
