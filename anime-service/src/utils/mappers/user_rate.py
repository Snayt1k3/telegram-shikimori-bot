from src.adapters.storage.models.user_rate import UserRateModel
from src.application.interfaces.mapper import AbstractMapper
from src.utils.mappers.title import TitleMapper
from src.domain.entities.user_rate import UserRateEntity


class UserRateMapper(AbstractMapper):
    @staticmethod
    def model_to_entity(model: UserRateModel) -> UserRateEntity:
        return UserRateEntity(
            id=model.id,
            title=TitleMapper.model_to_entity(model.title),
            target_id=model.target_id,
            target_type=model.target_type,
            score=model.score,
            status=model.status,
            episodes=model.episodes,
            chapters=model.chapters,
            rewatches=model.rewatches,
            volumes=model.volumes,
        )

    @staticmethod
    def entity_to_model(model: UserRateEntity) -> UserRateModel:
        return UserRateModel(
            id=model.id,
            title=TitleMapper.entity_to_model(model.title),
            target_id=model.target_id,
            target_type=model.target_type,
            score=model.score,
            status=model.status,
            episodes=model.episodes,
            chapters=model.chapters,
            rewatches=model.rewatches,
            volumes=model.volumes,
        )
