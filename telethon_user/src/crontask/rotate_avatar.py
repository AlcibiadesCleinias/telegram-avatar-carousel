from telethon import TelegramClient

from config.misc import redis
from config.settings import settings
from crontask.base import CronTaskBase
from telegram.change_avatar import change_avatar


def redis_key_to_current_image(phone: str):
    return f'current_image:{phone}'


def _get_next_image(phone: str, images: list[str]) -> str:
    current_image = redis.get(redis_key_to_current_image(phone))
    if not current_image:
        return images[0]

    for idx, image in enumerate(images):
        if image == current_image:
            return images[idx+1]


async def _change_image_to_next(client: TelegramClient, phone: str, image_paths: list[str]):
    new_image = _get_next_image(phone, image_paths)
    await change_avatar(client, new_image)
    return redis.set(redis_key_to_current_image(phone), new_image)


class RotateAvatarTask(CronTaskBase):
    def __init__(self, crontab_schedule: str, client: TelegramClient, phone: str, image_paths: list[str]):
        super().__init__(
            crontab_schedule,
            coro=_change_image_to_next,
            args=(client, phone, image_paths,),
        )
