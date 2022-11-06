from telethon import TelegramClient
from teleredis import RedisSession  # todo: to async
from config.settings import settings
import redis  # todo: to async


redis_connector = redis.Redis(  # todo: relocate
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=False,
)


async def get_telegram_client(api_key, api_hash, phone) -> TelegramClient:
    # TODO: use hash
    session = RedisSession(phone, redis_connector)
    client = TelegramClient(session, api_key, api_hash)
    await client.connect()
    return client
