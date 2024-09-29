from sqlalchemy import insert, update

from src.adapters.storage.repository.base import SQLAlchemyRepository
from src.adapters.storage.models.title import TitleModel
from src.domain.entities.title import TitleEntity
from src.utils.mappers.title import TitleMapper


class TitleRepo(SQLAlchemyRepository):
    model = TitleModel
    mapper = TitleMapper

    async def add_one(self, entity: TitleEntity) -> int:
        stmt = (
            insert(self.model)
            .values(
                id=entity.id,
                title_ru=entity.title_ru,
                title_en=entity.title_en,
                image_url=entity.image_url,
                status=entity.status,
                score=entity.score,
                episodes_aired=entity.episodes_aired,
                episodes=entity.episodes,
                volumes=entity.volumes,
                chapters=entity.chapters,
            )
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, entity: TitleEntity) -> TitleEntity:
        stmt = (
            update(self.model)
            .values(
                id=entity.id,
                title_ru=entity.title_ru,
                title_en=entity.title_en,
                image_url=entity.image_url,
                status=entity.status,
                score=entity.score,
                episodes_aired=entity.episodes_aired,
                episodes=entity.episodes,
                volumes=entity.volumes,
                chapters=entity.chapters,
            )
            .filter_by(id=entity.id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())
