from abc import abstractmethod, ABC
from typing import AsyncContextManager

from src.application.usecases import anime, user


class InteractorFactory(ABC):
    @abstractmethod
    def add_user(self) -> AsyncContextManager[user.AddUserUseCase]:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self) -> AsyncContextManager[user.DeleteUserUseCase]:
        raise NotImplementedError

    @abstractmethod
    def add_follow(self) -> AsyncContextManager[user.AddFollowUseCase]:
        raise NotImplementedError

    @abstractmethod
    def remove_follow(self) -> AsyncContextManager[user.DeleteFollowUseCase]:
        raise NotImplementedError

    @abstractmethod
    def all_follows(self) -> AsyncContextManager[user.GetAllFollowsUseCase]:
        raise NotImplementedError

    @abstractmethod
    def add_user_rate(self) -> AsyncContextManager[user.CreateUserRateUseCase]:
        raise NotImplementedError

    @abstractmethod
    def delete_user_rate(self) -> AsyncContextManager[user.DeleteUserRateUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_user_rates(self) -> AsyncContextManager[user.GetAllUserRates]:
        raise NotImplementedError

    @abstractmethod
    def update_user_rate(self) -> AsyncContextManager[user.UpdateUserRateUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_credentials(self) -> AsyncContextManager[user.GetCredentialsUseCase]:
        raise NotImplementedError

    @abstractmethod
    def anilibria_search(self) -> AsyncContextManager[anime.AnilibriaSearchUseCase]:
        raise NotImplementedError

    @abstractmethod
    def anilibria_get_torrent(self) -> AsyncContextManager[anime.GetTorrentUseCase]:
        raise NotImplementedError

    @abstractmethod
    def shikimori_search(self) -> AsyncContextManager[anime.ShikimoriSearchUseCase]:
        raise NotImplementedError

    @abstractmethod
    def shikimori_get_list(self) -> AsyncContextManager[anime.GetUserListUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_shikimori_uri(self) -> AsyncContextManager[user.GetURIUseCase]:
        raise NotImplementedError

    @abstractmethod
    def sync_user_rates(self) -> AsyncContextManager[user.SynchronizeUserRate]:
        raise NotImplementedError

    @abstractmethod
    def get_user_rate(self) -> AsyncContextManager[user.GetUserRate]:
        raise NotImplementedError

    @abstractmethod
    def get_anilibria_title(self) -> AsyncContextManager[anime.AnilibriaGetTitleUseCase]:
        raise NotImplementedError

    @abstractmethod
    def get_shikimori_title(self) -> AsyncContextManager[anime.ShikimoriGetAnimeUseCase]:
        raise NotImplementedError
