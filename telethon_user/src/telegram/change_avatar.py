from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest

from config.logger import get_app_logger

logger = get_app_logger()


async def change_avatar(client_inited: 'TelegramClient', image_path: str) -> int:
    """Return telegram image id of changed avatar."""
    async with await client_inited() as bot:
        return await bot(UploadProfilePhotoRequest(
            await bot.upload_file(image_path)
        ))
