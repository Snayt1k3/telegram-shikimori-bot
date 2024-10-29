from src.adapters.storage.models.title import TitleModel
from src.adapters.storage.repository.base import SQLAlchemyRepository
from src.utils.mappers.title import TitleMapper


class TitleRepo(SQLAlchemyRepository):
    model = TitleModel
    mapper = TitleMapper
