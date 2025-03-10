import json
from abc import ABC, abstractmethod
from logging import getLogger

from redis import asyncio as aioredis
from src.config.redis import RedisConfig

logger = getLogger(__name__)


class AbstractCache(ABC):
    """
    Interface for cache tools
    """

    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, data: dict | list, expire_in: int = 60 * 60):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError


class RedisCache(AbstractCache):

    def __init__(self, config: RedisConfig):
        self.cfg = config
        self.client = aioredis.from_url(self.cfg.url)

    async def get(self, key: str):
        try:
            logger.info(f"Getting data from redis for key - {key}")
            res = await self.client.get(key)
            logger.info(f"data successfully retrieved from redis for key - {key}")
            if res is not None:
                return json.loads(res)

        except Exception as e:
            logger.error(f"Error while getting data from redis for key - {key}, {e}")
            return {}

    async def set(self, key: str, data: dict | list, expire_in: int = 60 * 60):
        try:
            logger.info(f"setting data to redis for key - {key}")
            res = await self.client.set(key, json.dumps(data), ex=expire_in)
            logger.info(f"data successfully set to redis for key - {key}")
            return res

        except Exception as e:
            logger.error(f"Error while setting data to redis for key - {key}, {e}")
            return {}

    async def delete(self, key: str):
        try:
            logger.info(f"deleting data for key - {key}")
            res = await self.client.delete(key)
            logger.info(f"data was removed from redis - {key}")
            return res

        except Exception as e:
            logger.error(f"Error while deleting key from redis - {key}, {e}")
            return {}
