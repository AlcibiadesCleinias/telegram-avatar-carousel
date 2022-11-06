from typing import List

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from tg_avatar_carousel.telegram_avatars.models import CarouselImage, TelegramAvatarBot, TelegramProfile
from tg_avatar_carousel.utils.clients.telethon_user import post_change_avatar
from tg_avatar_carousel.utils.redisdb import redis, redis_key_to_current_image

logger = get_task_logger(__name__)


def _get_next_image(user_id: int, images: List[CarouselImage]) -> CarouselImage:
    assert images

    current_image = redis.get(redis_key_to_current_image(user_id))
    if not current_image:
        return images[0]

    for idx, image in enumerate(images):
        if image.id == current_image:
            return images[idx+1]



# from tg_avatar_carousel.telegram_avatars.tasks import periodic_rotate_user_avatar
@shared_task
def periodic_rotate_user_avatar(user_id: int):
    """Rotate user avatar periodically.
    By user id it gets image order and find the next to rotate to.
    # Flow
    User creates its telegram profile, on save
    """
    user = get_user_model().objects.select_related('telegram_profile__telegram_avatar_bot').get(pk=user_id)
    logger.info('Proceed timetabled carousel for user = %s', user)
    telegram_profile = TelegramProfile.objects.get(user=user)
    tg_bot = TelegramAvatarBot.objects.get(telegram_profile=telegram_profile)
    images = CarouselImage.objects.filter(telegram_avatar_bot=tg_bot).order_by('order')

    if not images:
        logger.info('No images for %s, pass', user)
        return

    new_image = _get_next_image(user_id, images)
    logger.info('Change avatar for %s on %d with url %s', user_id, new_image.id, new_image.image.url)

    post_change_avatar(
        api_key=telegram_profile.api_key,
        api_hash=telegram_profile.api_hash,
        phone=telegram_profile.phone,
        image_url='http://core:8000' + new_image.image.url,
    )
    # TODO: call client

