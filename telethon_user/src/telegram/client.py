from telethon import TelegramClient
from teleredis import RedisSession  # todo: to async
from config.settings import settings
import redis  # todo: to async


redis_connector = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=False,
)
session = RedisSession(settings.TG_API_PHONE, redis_connector)


async def get_telegram_client() -> TelegramClient:
    """Returns client, not connected."""
    client = TelegramClient(
        session, settings.TG_API_KEY, settings.TG_API_HASH,
    )
    return client
