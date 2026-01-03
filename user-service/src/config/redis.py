from src.config.base import BaseConfig


class RedisConfig(BaseConfig):
    REDIS_DB: int
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASS: str

    @property
    def url(self) -> str:
        return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


redis_cfg = RedisConfig()
