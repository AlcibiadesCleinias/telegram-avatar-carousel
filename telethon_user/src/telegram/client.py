from telethon import TelegramClient
from config.settings import settings
import redis  # todo: to async


redis_connector = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=False,
)
telegram_client = TelegramClient(
    'data_session/session', settings.TG_API_KEY, settings.TG_API_HASH,
)

async def get_telegram_client_inited() -> 'TelegramClient':
    """Returns client, not connected."""
    # TODO: hack with avaited
    return await telegram_client.start()
