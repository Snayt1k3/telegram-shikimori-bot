from typing import List

from src.application.interfaces.database.sql.base import BaseSqlRepository, UPDATE_TYPE, RETURN_TYPE, CREATE_TYPE


class AnimeRepository(BaseSqlRepository):
    async def get_by_id(self, id: int) -> RETURN_TYPE:
        raise NotImplementedError

    async def get_all(self) -> List[RETURN_TYPE]:
        raise NotImplementedError

    async def update_one(self, id: int, new_data: UPDATE_TYPE) -> RETURN_TYPE:
        raise NotImplementedError

    async def delete_one(self, id: int) -> RETURN_TYPE:
        raise NotImplementedError

    async def create_one(self, obj: CREATE_TYPE) -> RETURN_TYPE:
        raise NotImplementedError
