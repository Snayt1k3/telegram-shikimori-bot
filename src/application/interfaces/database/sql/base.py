from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

RETURN_TYPE = TypeVar("RETURN_TYPE")
CREATE_TYPE = TypeVar("CREATE_TYPE")
UPDATE_TYPE = TypeVar("UPDATE_TYPE")


class BaseSqlRepository(Generic[RETURN_TYPE, CREATE_TYPE, UPDATE_TYPE], ABC):
    """
    interface for sql database repository
    """
    @abstractmethod
    async def get_by_id(self, id: int) -> RETURN_TYPE:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[RETURN_TYPE]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, new_data: UPDATE_TYPE) -> RETURN_TYPE:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> RETURN_TYPE:
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, obj: CREATE_TYPE) -> RETURN_TYPE:
        raise NotImplementedError
