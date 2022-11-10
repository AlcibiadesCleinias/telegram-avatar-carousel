import logging

from telethon import TelegramClient
from telethon.errors import FilePart0MissingError
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from config.misc import redis
from utils.redis_storage import TelegramFileCacheStorage

logger = logging.getLogger(__name__)


async def change_avatar(client_inited: 'TelegramClient', image_path: str, delete_previous: bool = False) -> int:
    """Return telegram image id of changed avatar.
    Feature:
    - check in Redis for cache
    - delete previous if requested
    """
    async with await client_inited() as bot:
        if delete_previous:
            logger.info('Delete previous photo...')
            await bot(DeletePhotosRequest(await bot.get_profile_photos("me", limit=1)))

        logger.info('Upload new photo...')

        telegram_file_cache = TelegramFileCacheStorage(redisdb=redis, file_name=image_path)
        telegram_file_cached = await telegram_file_cache.get()
        if telegram_file_cached:
            logger.info('Found file %s in redis cache, use it...', image_path)
            tg_file = await telegram_file_cache.get()
            upload_file_request = UploadProfilePhotoRequest(tg_file)
            try:
                return await bot(upload_file_request)
            except FilePart0MissingError:
                logger.warning('Could not use cached file due to FilePart0MissingError, continue...')
                pass

        logger.info('Upload the file %s...', image_path)
        upload_file_request = UploadProfilePhotoRequest(
            await bot.upload_file(image_path)
        )
        logger.info('Save tg file %s into Redis cache...', image_path)
        await telegram_file_cache.save(upload_file_request.file)
        return await bot(upload_file_request)
