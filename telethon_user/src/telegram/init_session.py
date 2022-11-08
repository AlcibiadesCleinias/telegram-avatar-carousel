import logging
from typing import Optional

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config.misc import redis

logger = logging.getLogger(__name__)


async def request_code(client: TelegramClient, phone: str):
    if not await client.is_user_authorized():
        sent = await client.send_code_request(phone)
        logger.info(f'Send request for a phone_code_hash, got: {sent}')

        logger.info('Try to save the phone_code_hash hash into redis...')
        await redis.set(phone, sent.phone_code_hash)
    return request_code


async def post_code(client: TelegramClient, phone: str, user_code: str, user_password: Optional[str]):
    phone_code_hash = await redis.get(phone)
    logger.info('Phone code hash %s', phone_code_hash)
    signed = None

    try:
        signed = await client.sign_in(
            phone=phone,
            code=user_code,
            phone_code_hash=phone_code_hash,
        )
    except SessionPasswordNeededError:
        logger.warning('Could not login with user_code. Try to use user password if supplied...')
        signed = await client.sign_in(
            password=user_password,
        )
    except Exception as e:
        logger.exception(f'Could not proceed session init with {e}')

    return signed


async def init_session(client: TelegramClient, phone: str):
    """Complex convenience method that requires user action as well."""
    await request_code(client, phone)
    user_code = input('Enter code you received...\n')
    user_password = input('Enter password if you enable 2 step auth...\n')
    return await post_code(client, phone, user_code, user_password)
