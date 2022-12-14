import asyncio
import logging
from random import choice

from telethon import TelegramClient

from config.misc import redis
from crontask.base import CronTaskBase
from telegram.change_avatar import change_avatar

logger = logging.getLogger(__name__)


def redis_key_to_current_image(phone: str):
    return f'current_image:{phone}'


async def _get_next_image(phone: str, images: list[str]) -> (bool, str):
    """Returns tuple of if previous image known and next image."""
    current_image = await redis.get(redis_key_to_current_image(phone))
    logger.info('Current image according to Redis is %s', current_image)
    if not current_image:
        return bool(current_image), images[0]

    idx = 0
    images_len = len(images)
    while idx < images_len:
        if current_image == images[idx]:
            break
        idx += 1

    if idx == images_len:
        return bool(current_image), images[0]

    return bool(current_image), images[(idx + 1) % images_len]


async def change_image_to_next(
        client: TelegramClient,
        phone: str,
        image_paths: list[str],
        random_delay_period: int,
        try_cache: bool,
):
    """Implementation of image changing, i.e. avatar rotation.
    :param random_delay_period: choose seconds to sleep before actual rotation.
    :param try_cache: choose rather want to use cached telegram file meta first
    or go to upload file instantly.
    """
    is_previous, new_image = await _get_next_image(phone, image_paths)
    logger.info('Next image %s to change', new_image)
    to_sleep = choice(range(random_delay_period)) if random_delay_period else 0
    logger.info('Sleep before change: %s seconds...', to_sleep)
    await asyncio.sleep(to_sleep)
    changed = await change_avatar(client, new_image, try_cache=try_cache, delete_previous=is_previous)
    logger.info('Changed to %s', changed)
    image_set = await redis.set(redis_key_to_current_image(phone), new_image)
    return image_set


class RotateAvatarTask(CronTaskBase):
    def __init__(
            self,
            crontab_schedule: str,
            client: 'TelegramClient',
            phone: str,
            image_paths: list[str],
            random_delay_period: int = 0,
            try_cache: bool = True,
    ):
        super().__init__(
            crontab_schedule,
            coro=change_image_to_next,
            args=(client, phone, image_paths, random_delay_period, try_cache,),
        )
