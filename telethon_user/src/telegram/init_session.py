import logging

from telethon import TelegramClient

logger = logging.getLogger(__name__)


async def _get_me(client):
    me = await client.get_me()
    logger.info(f'U logged as {me.username}')


def init_session(client: TelegramClient):
    """Convenience method that requires user action to login."""
    logger.info('Init session via connect to event loop & call get_me...')
    with client:
        client.loop.run_until_complete(_get_me(client))
