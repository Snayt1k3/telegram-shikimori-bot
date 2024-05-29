from dataclasses import asdict

from src.application.dto.title.list import UserListDTO
from src.application.dto.user.user import UserRateDTO
from src.application.enums.shikimori import ShikimoriListType
from src.application.interfaces.cache import AbstractCache
from src.application.interfaces.database.uow import AbstractUnitOfWork
from src.application.interfaces.usecases import UseCase
from src.domain.user import UserEntity


class GetUserListUseCase(UseCase):
    """
    getting user list from shikimori and inserting hin into redis
    """

    def __init__(self, uow: AbstractUnitOfWork, cache: AbstractCache):
        self.uow = uow
        self.cache = cache

    async def __call__(
        self, id_telegram: int, listType: ShikimoriListType
    ) -> UserListDTO:

        if data := await self.cache.get(f"{id_telegram} {str(listType)}"):
            return UserListDTO.from_dict(data)

        async with self.uow:
            user: UserEntity = await self.uow.user.find_one(id_telegram=id_telegram)

        rates = user.get_user_rates_by_status(str(listType))

        result = UserListDTO(
            [UserRateDTO.from_dict(asdict(rate)) for rate in rates],
            listType,
            length=len(rates),
        )

        await self.cache.set(f"{id_telegram} {str(listType)}", asdict(result))

        return result
