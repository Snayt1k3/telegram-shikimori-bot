from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.user_rate.orm import UserRate


class UserRateRepository(SQLAlchemyRepository):
    model = UserRate
