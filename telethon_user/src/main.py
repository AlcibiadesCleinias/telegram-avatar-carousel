import argparse
import asyncio
from logging.config import dictConfig

from config.logger import get_app_logger
from config.settings import settings, LOGGING
from crontask.rotate_avatar import RotateAvatarTask
from telegram.client import get_telegram_client
from telegram.init_session import init_session
from utils.image_files import get_all_images

dictConfig(LOGGING)
logger = get_app_logger()


async def main(args):
    client = await get_telegram_client()
    await client.connect()

    if args.init_session:
        logger.info('Init session...')
        try:
            return await init_session(client=client, phone=settings.TG_API_PHONE)
        except Exception as e:
            logger.exception('Could not init session. Return...')
    else:
        all_images = get_all_images(settings.DATA_AVATARS)
        if not all_images:
            logger.warning('No images in %s. Return...', settings.DATA_AVATARS)
            return

        logger.info(
            'Start avatar jon rotation for avatars: %s with crontab %s', all_images, settings.ROTATE_AVATAR_TASK_CORO,
        )
        RotateAvatarTask(
            crontab_schedule=settings.ROTATE_AVATAR_TASK_CORO,
            client=client,
            phone=settings.TG_API_PHONE,
            image_paths=all_images,
        )

    await client.disconnect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--init-session', type=bool, default=False,
                        help="Define if you want to merely init session.")

    args, unparsed = parser.parse_known_args()
    if unparsed and len(unparsed) > 0:
        logger.warning('Unparsed arguments %s. Assert...', unparsed)
        assert False

    asyncio.run(main(args))
