from src.application.interfaces.database.mapper import AbstractMapper
from src.domain.title import TitleEntity
from src.adapters.database.sql.title.orm import Title


class TitleMapper(AbstractMapper):
    @staticmethod
    def entity_to_model(model: TitleEntity) -> Title:
        return Title(
            id=model.id,
            target_id=model.target_id,
            title_ru=model.title_ru,
            title_en=model.title_en,
            chapters=model.chapters,
            episodes=model.episodes,
            episodes_aired=model.episodes_aired,
            status=model.status,
            score=model.score,
            volumes=model.volumes,
            image_url=model.image_url
        )

    @staticmethod
    def model_to_entity(model: Title) -> TitleEntity:
        return TitleEntity(
            id=model.id,
            target_id=model.target_id,
            title_ru=model.title_ru,
            title_en=model.title_en,
            chapters=model.chapters,
            episodes=model.episodes,
            episodes_aired=model.episodes_aired,
            status=model.status,
            score=model.score,
            volumes=model.volumes,
            image_url=model.image_url
        )
