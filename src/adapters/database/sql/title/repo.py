from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.title.orm import Title


class TitleRepository(SQLAlchemyRepository):
    model = Title
