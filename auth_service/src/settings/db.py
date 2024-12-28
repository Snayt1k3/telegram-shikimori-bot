from src.settings.base import Settings


class DBSettings(Settings):
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None
    POSTGRES_DB: str = None
    POSTGRES_HOST: str = None

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"


db_settings = DBSettings()
