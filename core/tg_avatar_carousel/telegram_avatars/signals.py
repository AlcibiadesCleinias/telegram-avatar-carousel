from django.db.models.signals import pre_save
from django.dispatch import receiver

from tg_avatar_carousel.telegram_avatars.models import TelegramAvatarBot


# TODO: why in signal. To form
@receiver(pre_save, sender=TelegramAvatarBot)
def set_args_as_user_id(sender, instance: TelegramAvatarBot, *args, **kwargs):
    # TODO: secure problem: other one could possible change tg. profile
    telegram_profile = instance.telegram_profile

    if telegram_profile:
        user_id = telegram_profile.user.id
        instance.args = [user_id]
        instance.task = 'tg_avatar_carousel.telegram_avatars.tasks.periodic_rotate_user_avatar'
        instance.save()

