import logging

from telethon import TelegramClient

from config.misc import redis
from crontask.base import CronTaskBase
from telegram.change_avatar import change_avatar

logger = logging.getLogger(__name__)


def redis_key_to_current_image(phone: str):
    return f'current_image:{phone}'


async def _get_next_image(phone: str, images: list[str]) -> str:
    current_image = await redis.get(redis_key_to_current_image(phone))
    logger.info('Current image according to Redis is %s', current_image)
    if not current_image:
        return images[0]

    idx = 0
    images_len = len(images)
    while idx < images_len:
        if current_image == images[idx]:
            break
        idx += 1

    if idx == images_len:
        return images[0]

    return images[(idx + 1) % images_len]


async def _change_image_to_next(client: TelegramClient, phone: str, image_paths: list[str]):
    new_image = await _get_next_image(phone, image_paths)
    logger.info('Next image %s to change', new_image)
    await change_avatar(client, new_image)
    image_set = await redis.set(redis_key_to_current_image(phone), new_image)
    return image_set


class RotateAvatarTask(CronTaskBase):
    def __init__(self, crontab_schedule: str, client: 'TelegramClient', phone: str, image_paths: list[str]):
        super().__init__(
            crontab_schedule,
            coro=_change_image_to_next,
            args=(client, phone, image_paths,),
        )
