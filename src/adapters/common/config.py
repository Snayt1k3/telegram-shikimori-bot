import os


class Config:
    SHIKI_UA = os.getenv("SHIKI_UA")
    CLIENT_SECRET = os.getenv("SHIKI_CLIENT_SECRET")
    CLIENT_ID = os.getenv("SHIKI_CLIENT_ID")
