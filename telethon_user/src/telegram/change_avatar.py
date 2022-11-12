import asyncio
import logging

from telethon import TelegramClient
from telethon.errors import FilePart0MissingError
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from config.misc import redis
from utils.image_files import generate_random_filename
from utils.redis_storage import TelegramFileCacheStorage

logger = logging.getLogger(__name__)


async def change_avatar(
        client_inited: 'TelegramClient',
        image_path: str,
        try_cache: bool = False,
        delete_previous: bool = False,
) -> int:
    """Return telegram image id of changed avatar.
    Feature:
    - check in Redis for file cached meta (that telegram returns on file saved)
    - delete previous if requested
    """
    async with await client_inited() as bot:
        telegram_file_cache = TelegramFileCacheStorage(redisdb=redis, file_name=image_path)
        telegram_file_cached = await telegram_file_cache.get() if try_cache else None
        changed_avatar = None

        logger.info('Start avatar change process...')
        if telegram_file_cached:
            logger.info('Found file %s in redis cache, use it...', image_path)
            tg_file = await telegram_file_cache.get()
            upload_file_request = UploadProfilePhotoRequest(tg_file)
            try:
                changed_avatar = await bot(upload_file_request)
            except FilePart0MissingError:
                logger.warning('Could not use cached file due to FilePart0MissingError, continue...')
                pass

        if not changed_avatar:
            logger.info('Upload new file %s to telegram...', image_path)
            upload_file_request = UploadProfilePhotoRequest(
                await bot.upload_file(image_path, file_name=generate_random_filename(image_path))
            )
            logger.info('Save tg file %s into Redis cache...', image_path)
            await telegram_file_cache.save(upload_file_request.file)
            changed_avatar = await bot(upload_file_request)

        # Delete previous old photo at the end of rotate action.
        if delete_previous:
            # Lets sleep to not hit tg limit.
            await asyncio.sleep(1)
            logger.info('Delete previous photo after uploaded the new one...')
            photos = await bot.get_profile_photos("me", offset=1, limit=1)
            logger.info('Fetched previous photos, got %s', photos)
            await bot(DeletePhotosRequest(photos))

        return changed_avatar
