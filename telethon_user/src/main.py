import argparse
import asyncio
import logging
from logging.config import dictConfig

from config.settings import settings, LOGGING
from crontask.rotate_avatar import RotateAvatarTask, change_image_to_next
from telegram.client import telegram_client, get_telegram_client_inited
from telegram.init_session import init_session
from utils.image_files import get_all_images

dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def main(args):
    """Rather init session or start avatar rotate task."""
    if args.init_session:
        return init_session(telegram_client)

    all_images = get_all_images(settings.DATA_AVATARS)
    if not all_images:
        logger.warning('No images in %s. Return...', settings.DATA_AVATARS)
        return

    if args.rotate_once:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(change_image_to_next(
            client=get_telegram_client_inited,
            phone=settings.TG_API_PHONE, image_paths=all_images, random_delay_period=0,
            try_cache=settings.TASK_TRY_CACHE_FIRST),
        )
    else:
        logger.info(
            'Start task avatar rotation. Avatars %s with crontab %s', all_images, settings.ROTATE_AVATAR_TASK_CORO,
        )
        RotateAvatarTask(
            crontab_schedule=settings.ROTATE_AVATAR_TASK_CORO,
            client=get_telegram_client_inited,
            phone=settings.TG_API_PHONE,
            image_paths=all_images,
            random_delay_period=settings.TASK_RANDOM_DELAY_PERIOD,
            try_cache = settings.TASK_TRY_CACHE_FIRST,
        ).start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-session', type=bool, default=False,
                        help="Define if you want to merely init session.")
    parser.add_argument('--rotate-once', type=bool, default=False,
                        help="Define if you want to merely run rotation once.")

    args, unparsed = parser.parse_known_args()
    if unparsed and len(unparsed) > 0:
        logger.warning('Unparsed arguments %s. Assert...', unparsed)
        assert False

    main(args)
