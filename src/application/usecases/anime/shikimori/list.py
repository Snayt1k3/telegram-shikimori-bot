from dataclasses import asdict

from src.application.dto.title.list import UserListDTO
from src.application.dto.user.user import UserRateDTO
from src.application.enums.shikimori import ShikimoriListType
from src.application.interfaces.database.uow import AbstractUnitOfWork
from src.application.interfaces.usecases import UseCase
from src.domain.user import UserEntity


class GetUserListUseCase(UseCase):
    """
    getting user list from shikimori and inserting hin into redis
    """

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
        self.cache = None  # todo add cache repo

    async def __call__(
        self, id_telegram: int, listType: ShikimoriListType
    ) -> UserListDTO:

        # TODO проверка на наличие в cache

        async with self.uow:
            user: UserEntity = await self.uow.user.find_one(id_telegram=id_telegram)

        rates = user.get_user_rates_by_status(str(listType))

        return UserListDTO(
            [UserRateDTO.from_dict(asdict(rate)) for rate in rates],
            listType,
            length=len(rates),
        )
