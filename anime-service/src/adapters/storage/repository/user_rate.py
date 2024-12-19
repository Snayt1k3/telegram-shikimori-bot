from src.adapters.storage.models.user_rate import UserRateModel
from src.adapters.storage.repository.base import SQLAlchemyRepository


class UserRateRepo(SQLAlchemyRepository):
    model = UserRateModel
