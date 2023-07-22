from database.schemas.base import Base


class UserAuth(Base):
    """
    responsible for types of data Shikimori auth
    """
    shikimori_id: int = None
    access_token: str = ""
    refresh_token: str = ""
    auth_token: str = ""


class UserFollows(Base):
    """
    responsible for types of data user follows
    """
    follows: list[int] = None
