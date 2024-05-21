from logging import getLogger

from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.notifications.orm import (
    Notification,
    AnilibriaAnime,
)

logger = getLogger("repo.notifications")


class NotificationsRepository(SQLAlchemyRepository):
    model = Notification


class AnilibriaAnimeRepository(SQLAlchemyRepository):
    model = AnilibriaAnime
