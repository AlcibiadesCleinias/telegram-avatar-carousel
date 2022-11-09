import logging

from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest


logger = logging.getLogger(__name__)


async def change_avatar(client_inited: 'TelegramClient', image_path: str, delete_previous: bool = False) -> int:
    """Return telegram image id of changed avatar."""
    async with await client_inited() as bot:
        if delete_previous:
            logger.info('Delete previous photo...')
            await bot(DeletePhotosRequest(await bot.get_profile_photos("me", limit=1)))

        logger.info('Upload new photo...')
        return await bot(UploadProfilePhotoRequest(
            await bot.upload_file(image_path)
        ))
