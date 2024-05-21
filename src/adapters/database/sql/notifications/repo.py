from logging import getLogger

from src.application.interfaces.database.sql.base import BaseSqlRepository

logger = getLogger("repo.notifications")


class NotificationsRepository(
    BaseSqlRepository
):
    pass

class AnilibriaAnimeRepository(BaseSqlRepository):
    pass