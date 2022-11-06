from django.contrib import admin
from django.utils.html import format_html

from django.utils.translation import gettext_lazy as _

from tg_avatar_carousel.telegram_avatars.models import TelegramProfile, CarouselImage, TelegramAvatarBot


def resize_width(old_width, old_height, new_heigh):
    """Return new width (save proportions)"""
    return int(old_width * new_heigh / old_height)


class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'phone')


class ImageTagDisplayMixin:
    def image_tag(self, obj):
        new_h = 200
        new_w = resize_width(old_width=obj.image.width, old_height=obj.image.height, new_heigh=new_h)
        return (
            format_html(
                '<a href={url} target="_blank"><img src="{url}" width="{width}" height="{height}" /></a>'.format(
                    url=obj.image.url, width=new_w, height=new_h))
        )
    image_tag.short_description = _('Show photo 1')


class CarouselImageAdmin(ImageTagDisplayMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['telegram_avatar_bot', 'image', 'image_tag', 'order']}),
    ]
    list_display = ['image', 'telegram_avatar_bot', 'image_tag', 'order']
    readonly_fields = ['image_tag']


class CarouselImageInline(ImageTagDisplayMixin, admin.TabularInline):
    model = CarouselImage
    extra = 5
    fields = ('image', 'image_tag', 'order')
    readonly_fields = ['image_tag']


class TelegramAvatarBotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['telegram_profile', 'name', 'crontab']}),
    ]
    inlines = [CarouselImageInline]
    list_display = ['telegram_profile', 'name']


admin.site.register(TelegramAvatarBot, TelegramAvatarBotAdmin)
admin.site.register(TelegramProfile, TelegramProfileAdmin)
admin.site.register(CarouselImage, CarouselImageAdmin)
