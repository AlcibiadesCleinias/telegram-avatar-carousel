from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tg_avatar_carousel.telegram_avatars.urls', namespace='users')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

# TODO: solve problem with media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
