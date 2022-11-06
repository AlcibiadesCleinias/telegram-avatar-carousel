from django.urls import path

from tg_avatar_carousel.telegram_avatars import views

app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/telegram-user', views.TelegramUserListView.as_view(), name='telegram_user'),
    path('api/auth/request-code', views.TelegramUserRequestCodeAPIView.as_view(), name='telegram_request_code'),
    path('api/auth/enter-code', views.TelegramEnterCodeAPIView.as_view(), name='telegram_enter_code'),
]
