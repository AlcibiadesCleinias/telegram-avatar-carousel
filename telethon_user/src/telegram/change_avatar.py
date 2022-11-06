from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest

from config.logger import get_app_logger

logger = get_app_logger()


async def change_avatar(client: TelegramClient, image_path: str) -> int:
    """Return telegram image id of changed avatar."""
    return await client(UploadProfilePhotoRequest(
        await client.upload_file(image_path)
    ))
