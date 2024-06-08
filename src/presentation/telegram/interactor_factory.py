from abc import abstractmethod, ABC
from typing import AsyncContextManager

from src.application.usecases.anime import (
    AnilibriaSearchUseCase,
    GetTorrentUseCase,
    ShikimoriSearchUseCase,
    GetUserListUseCase,
)
from src.application.usecases.user import (
    AddUserUseCase,
    DeleteUserUseCase,
    AddFollowUseCase,
    DeleteFollowUseCase,
    GetAllFollowsUseCase,
    CreateUserRateUseCase,
    DeleteUserRateUseCase,
    GetAllUserRates,
    UpdateUserRateUseCase,
    GetCredentialsUseCase,
    GetURIUseCase,
    SynchronizeUserRate,
)


class InteractorFactory(ABC):
    @abstractmethod
    def add_user(self) -> AsyncContextManager[AddUserUseCase]:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self) -> AsyncContextManager[DeleteUserUseCase]:
        raise NotImplementedError

    @abstractmethod
    def add_follow(self) -> AsyncContextManager[AddFollowUseCase]:
        raise NotImplementedError

    @abstractmethod
    def remove_follow(self) -> AsyncContextManager[DeleteFollowUseCase]:
        raise NotImplementedError

    @abstractmethod
    def all_follows(self) -> AsyncContextManager[GetAllFollowsUseCase]:
        raise NotImplementedError

    @abstractmethod
    def add_user_rate(self) -> AsyncContextManager[CreateUserRateUseCase]:
        raise NotImplementedError

    @abstractmethod
    def delete_user_rate(self) -> AsyncContextManager[DeleteUserRateUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_user_rates(self) -> AsyncContextManager[GetAllUserRates]:
        raise NotImplementedError

    @abstractmethod
    def update_user_rate(self) -> AsyncContextManager[UpdateUserRateUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_credentials(self) -> AsyncContextManager[GetCredentialsUseCase]:
        raise NotImplementedError

    @abstractmethod
    def anilibria_search(self) -> AsyncContextManager[AnilibriaSearchUseCase]:
        raise NotImplementedError

    @abstractmethod
    def anilibria_get_torrent(self) -> AsyncContextManager[GetTorrentUseCase]:
        raise NotImplementedError

    @abstractmethod
    def shikimori_search(self) -> AsyncContextManager[ShikimoriSearchUseCase]:
        raise NotImplementedError

    @abstractmethod
    def shikimori_get_list(self) -> AsyncContextManager[GetUserListUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_shikimori_uri(self) -> AsyncContextManager[GetURIUseCase]:
        raise NotImplementedError

    @abstractmethod
    def sync_user_rates(self) -> AsyncContextManager[SynchronizeUserRate]:
        raise NotImplementedError
