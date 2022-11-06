from django.apps import AppConfig


class TelegramAvatarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tg_avatar_carousel.telegram_avatars'
    # signals_ready = False

    # def ready(self):
    #     self.check_dependences()
    #     if not self.signals_ready:
    #         from . import signals  # NOQA
    #         self.signals_ready = True
