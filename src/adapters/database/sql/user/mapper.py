from src.adapters.database.sql.user.orm import User, ShikiCredential, UserRate
from src.application.interfaces.database.sql.mapper import AbstractMapper
from src.domain.user import UserEntity, ShikiCredsEntity, UserRateEntity
from src.adapters.database.sql.title.mapper import TitleMapper


class UserRateMapper(AbstractMapper):
    @staticmethod
    def model_to_entity(model: UserRate) -> UserRateEntity:
        return UserRateEntity(
            id=model.id,
            user_rate_id=model.user_rate_id,
            follows=model.follows,
            user=UserMapper.model_to_entity(model.user),
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
    def entity_to_model(model: UserRateEntity) -> UserRate:
        return UserRate(
            id=model.id,
            user_rate_id=model.user_rate_id,
            user=UserMapper.entity_to_model(model.user),
            title=TitleMapper.entity_to_model(model.title),
            target_id=model.target_id,
            target_type=model.target_type,
            score=model.score,
            status=model.status,
            episodes=model.episodes,
            chapters=model.chapters,
            rewatches=model.rewatches,
            volumes=model.volumes,
            follows=model.follows,
        )


class CredsMapper(AbstractMapper):

    @staticmethod
    def model_to_entity(model: ShikiCredential) -> ShikiCredsEntity:
        return ShikiCredsEntity(
            id=model.id,
            access=model.access,
            refresh=model.refresh,
            expire_in=model.expire_in,
        )

    @staticmethod
    def entity_to_model(model: ShikiCredsEntity) -> ShikiCredential:
        return ShikiCredential(
            id=model.id,
            access=model.access,
            refresh=model.refresh,
            expire_in=model.expire_in,
        )


class UserMapper(AbstractMapper):

    @staticmethod
    def model_to_entity(model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            shiki_id=model.shiki_id,
            id_telegram=model.id_telegram,
            creds=CredsMapper.model_to_entity(model.creds),
            user_rates=[
                UserRateMapper.model_to_entity(rate) for rate in model.user_rates
            ],
            nickname=model.nickname,
            avatar=model.avatar,
        )

    @staticmethod
    def entity_to_model(model: UserEntity) -> User:
        return User(
            id=model.id,
            shiki_id=model.shiki_id,
            id_telegram=model.id_telegram,
            creds=CredsMapper.entity_to_model(model.creds),
            user_rates=[
                UserRateMapper.entity_to_model(rate) for rate in model.user_rates
            ],
            nickname=model.nickname,
            avatar=model.avatar,
        )
