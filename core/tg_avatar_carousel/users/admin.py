from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tg_avatar_carousel.users.models import User


admin.site.register(User, UserAdmin)
