from src.application.interfaces.mapper import AbstractMapper
from src.domain.entities.title import TitleEntity
from src.adapters.storage.models.title import TitleModel


class TitleMapper(AbstractMapper):
    @staticmethod
    def entity_to_model(model: TitleEntity) -> TitleModel:
        return TitleModel(
            id=model.id,
            title_ru=model.title_ru,
            title_en=model.title_en,
            chapters=model.chapters,
            episodes=model.episodes,
            episodes_aired=model.episodes_aired,
            status=model.status,
            score=model.score,
            volumes=model.volumes,
            image_url=model.image_url,
        )

    @staticmethod
    def model_to_entity(model: TitleModel) -> TitleEntity:
        return TitleEntity(
            id=model.id,
            title_ru=model.title_ru,
            title_en=model.title_en,
            chapters=model.chapters,
            episodes=model.episodes,
            episodes_aired=model.episodes_aired,
            status=model.status,
            score=model.score,
            volumes=model.volumes,
            image_url=model.image_url,
        )
