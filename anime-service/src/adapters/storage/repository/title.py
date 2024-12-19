from src.adapters.storage.models.title import TitleModel
from src.adapters.storage.repository.base import SQLAlchemyRepository


class TitleRepo(SQLAlchemyRepository):
    model = TitleModel
