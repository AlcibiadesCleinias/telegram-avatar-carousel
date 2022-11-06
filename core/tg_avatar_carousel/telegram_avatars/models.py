#  from tg_avatar_carousel.telegram_avatars.models import TelegramAvatarBot
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask

from tg_avatar_carousel.users.models import User


class TelegramProfile(models.Model):
    api_key = models.PositiveIntegerField()
    api_hash = models.CharField(max_length=256)
    phone = models.CharField(max_length=36, unique=True)

    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='telegram_profile',
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.phone} #{self.id}'


class TelegramAvatarBot(PeriodicTask):
    """Model that is designed to control access for a user for 1 cron task (per user)
    to rotate avatar images.

    On signal save it update or create PeriodicTask model for a user and proxies its crontab
    and user id to args of a task.
    """
    telegram_profile = models.OneToOneField(
        TelegramProfile, on_delete=models.CASCADE, related_name='telegram_avatar_bot',
    )

    def save(self, *args, **kwargs):
        telegram_profile = self.telegram_profile
        if telegram_profile:
            user_id = telegram_profile.user.id
            self.args = [user_id]
            self.task = 'tg_avatar_carousel.telegram_avatars.tasks.periodic_rotate_user_avatar'

        return super().save(*args, **kwargs)


class CarouselImage(models.Model):
    telegram_avatar_bot = models.ForeignKey(TelegramAvatarBot, on_delete=models.CASCADE,related_name='carousel_images')
    order = models.PositiveSmallIntegerField(_('Define your custom order'))
    image = models.ImageField(_('Your Picture'), blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.telegram_avatar_bot.telegram_profile.phone} #{self.id}'
