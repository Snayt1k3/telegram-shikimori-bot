from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.user.orm import User


class UserRepository(SQLAlchemyRepository):
    model = User
