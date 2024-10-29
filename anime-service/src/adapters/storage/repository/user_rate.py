from src.adapters.storage.models.user_rate import UserRateModel
from src.adapters.storage.repository.base import SQLAlchemyRepository
from src.utils.mappers.user_rate import UserRateMapper


class UserRateRepo(SQLAlchemyRepository):
    model = UserRateModel
    mapper = UserRateMapper
