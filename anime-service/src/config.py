import os


class Config:
    SHIKI_UA: str = os.getenv("SHIKI_UA")
    CLIENT_SECRET: str = os.getenv("SHIKI_CLIENT_SECRET")
    CLIENT_ID: str = os.getenv("SHIKI_CLIENT_ID")
