import os


class ShikimoriCfg:
    SHIKI_UA = os.getenv("SHIKI_UA")
    CLIENT_SECRET = os.getenv("SHIKI_CLIENT_SECRET")
    CLIENT_ID = os.getenv("SHIKI_CLIENT_ID")


class RedisCfg:
    DB = os.getenv("DB")
    HOST = os.getenv("REDIS_HOST")
    PORT = os.getenv("REDIS_PORT", 6379)
    PASS = os.getenv("REDIS_PASS")

    @property
    def url(self) -> str:
        return f"redis://:{self.PASS}@{self.HOST}:{self.PORT}/{self.DB}"
