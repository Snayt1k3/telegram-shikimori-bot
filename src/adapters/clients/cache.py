import json
from logging import getLogger

import aioredis

from src.adapters.common.config import RedisCfg
from src.application.interfaces.cache import AbstractCache

logger = getLogger(__name__)


class RedisCache(AbstractCache):

    def __init__(self, config: RedisCfg):
        self.cfg = config
        self.client = aioredis.from_url(self.cfg.url)

    async def get(self, key: str):
        try:
            logger.info(f"getting data from redis for key - {key}")
            res = await self.client.get(key)

            return json.loads(res)

        except Exception as e:
            logger.error(f"Error while getting data from redis for key - {key}, {e}")
            return {}

    async def set(self, key: str, data: dict, expire_in: int = 60 * 60):
        try:
            logger.info(f"setting data to redis for key - {key}")
            res = await self.client.set(key, json.dumps(data), ex=expire_in)
            return res

        except Exception as e:
            logger.error(f"Error while setting data to redis for key - {key}, {e}")
            return {}

    async def delete(self, key: str):
        try:
            logger.info(f"deleting key from redis - {key}")
            res = await self.client.delete(key)
            return res

        except Exception as e:
            logger.error(f"Error while delete key from redis - {key}, {e}")
            return {}
