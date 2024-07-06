import datetime
from dataclasses import dataclass
from typing import List

from black import Optional

from src.application.dto.user.user import (
    UserUpdateDTO,
    ShikiCredsDTO,
    UserRateUpdateDTO,
)
from src.domain.base import BaseEntity
from src.domain.title import TitleEntity


@dataclass
class ShikiCredsEntity(BaseEntity):
    id: Optional[int]
    access: str
    refresh: str
    expire_in: datetime.datetime

    def is_expired(self) -> bool:
        """Checking creds expire time"""
        if self.expire_in - datetime.datetime.now() > datetime.timedelta(hours=1):
            return True
        return False

    def update_creds(
        self, refresh: str, access: str, created_at: int
    ) -> "ShikiCredsEntity":
        self.refresh = refresh
        self.access = access
        self.expire_in = datetime.datetime.fromtimestamp(
            created_at
        ) + datetime.timedelta(days=1)

        return self

    @classmethod
    def create(cls, access: str, refresh: str, expire_in: int) -> "ShikiCredsEntity":
        return cls(
            id=None,
            access=access,
            refresh=refresh,
            expire_in=datetime.datetime.fromtimestamp(expire_in)
            + datetime.timedelta(days=1),
        )


@dataclass
class UserEntity(BaseEntity):
    id: Optional[int]
    id_telegram: int
    nickname: str
    avatar: str
    creds: ShikiCredsEntity
    user_rates: List["UserRateEntity"]
    follows: List[int]
    allow_notifications: bool = True

    def update_user(self, user: UserUpdateDTO) -> None:
        self.avatar = user.avatar
        self.nickname = user.nickname
        self.allow_notifications = user.allow_notifications

    @classmethod
    def create(
        cls,
        id: int,
        id_telegram: int,
        nickname: str,
        avatar: str,
        creds: ShikiCredsEntity,
        user_rates: List["UserRateEntity"],
        follows: List[int],
        allow_notifications: bool = True,
    ) -> "UserEntity":
        return cls(
            id=id,
            id_telegram=id_telegram,
            nickname=nickname,
            avatar=avatar,
            creds=creds,
            user_rates=user_rates,
            follows=follows,
            allow_notifications=allow_notifications,
        )

    def update_user_rate(self, user_rate: UserRateUpdateDTO) -> None:
        for rate in self.user_rates:
            if rate.id == user_rate.id:
                rate.update(user_rate)
                return

    def check_exists_user_rate(self, target_id: int, target_type: str) -> bool:
        for u in self.user_rates:
            if u.target_id == target_id and target_type == u.target_id:
                return True
        return False

    def get_user_rates_by_status(self, status: str) -> list["UserRateEntity"]:
        return [u for u in self.user_rates if u.status == status]

    def update_creds(self, creds: ShikiCredsDTO) -> None:
        self.creds.update_creds(
            creds.access,
            creds.refresh,
            datetime.datetime.fromtimestamp(creds.expire_in),
        )

    def add_follow(self, id: int) -> None:
        follows = set(self.follows)

        if id not in follows:
            self.follows.append(id)

    def remove_follow(self, id: int) -> None:
        follows = set(self.follows)

        if id in follows:
            self.follows.remove(id)


@dataclass
class UserRateEntity(BaseEntity):
    id: Optional[int]
    user: UserEntity
    title: TitleEntity
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]

    def update(self, new: UserRateUpdateDTO):
        self.score = new.score
        self.status = new.status
        self.chapters = new.chapters
        self.volumes = new.volumes
        self.rewatches = new.rewatches
        self.episodes = new.episodes

    @classmethod
    def create(
        cls,
        id: int,
        user: UserEntity,
        title: TitleEntity,
        target_id: int,
        target_type: str,
        score: int,
        status: str,
        episodes: Optional[int] = None,
        chapters: Optional[int] = None,
        volumes: Optional[int] = None,
        rewatches: Optional[int] = None,
    ) -> "UserRateEntity":
        return cls(
            id=id,
            user=user,
            title=title,
            target_id=target_id,
            target_type=target_type,
            score=score,
            status=status,
            episodes=episodes,
            chapters=chapters,
            volumes=volumes,
            rewatches=rewatches,
        )

    def is_up_to_date(self, new: UserRateUpdateDTO) -> bool:
        return all(
            [
                self.score == new.score,
                self.status == new.status,
                self.chapters == new.chapters,
                self.rewatches == new.rewatches,
                self.episodes == new.episodes,
                self.volumes == new.volumes,
            ]
        )
