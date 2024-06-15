from sqlalchemy import update, insert

from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.title.orm import Title
from src.domain.title import TitleEntity


class TitleRepository(SQLAlchemyRepository[TitleEntity]):
    model = Title

    async def add_one(self, entity: TitleEntity) -> int:
        stmt = (
            insert(self.model)
            .values(
                target_id=entity.target_id,
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
                target_id=entity.target_id,
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
