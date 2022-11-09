import json
from typing import Optional

from aioredis import Redis
from telethon.tl.types import InputFile

from config.misc import redis


class TelegramFileCacheStorage:
    def __init__(self, redisdb: Redis, file_name: str):
        self.redisdb = redisdb
        self.file_name = file_name

    async def get(self) -> Optional[InputFile]:
        tg_file = await redis.get(self.file_name)
        if not tg_file:
            return
        return InputFile(**json.loads(tg_file))

    async def save(self, tg_file: InputFile):
        tg_file = tg_file.to_dict()
        tg_file.pop('_', None)
        return await self.redisdb.set(self.file_name, json.dumps(tg_file))
