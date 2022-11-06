"""Seems that this views are fully solved init telegram session in telethon app.
TODO: relocate to separate logic app
"""
import logging

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tg_avatar_carousel.telegram_avatars.models import TelegramProfile
from tg_avatar_carousel.telegram_avatars.serializers import TelegramRequestCodeSerializer, TelegramProfileSerializer, \
    TelegramEnterCodeSerializer
from tg_avatar_carousel.utils.clients.telethon_user import post_telegram_code, request_telegram_code

logger = logging.getLogger(__name__)


USER_TG_CREDS_NOT_EXISTS_ERROR = 'User has not entered telegram profile.'
USER_TG_CREDS_NOT_CORRECT = 'User has not enough rights.'


class IndexView(TemplateView):
    template_name = 'tg_avatar_carousel/index.html'


class TelegramUserListView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TelegramProfileSerializer
    queryset = TelegramProfile.objects.all()


class TelegramUserRequestCodeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        """User enter the code he received. Thus it init session for auto operations."""
        qs = get_user_model().objects.all()
        user = qs.select_related('telegram_profile').get(id=request.user.id)

        serializer = TelegramRequestCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Check user rights
        tg_profile = get_object_or_404(TelegramProfile, phone=validated_data['phone'])
        if tg_profile.user.id is not user.id:
            raise ValidationError(USER_TG_CREDS_NOT_CORRECT)

        logger.info(f'Send request for code through telethon for user: {user}...')
        request_telegram_code(
            api_key=validated_data['api_key'],
            api_hash=validated_data['api_hash'],
            phone=validated_data['phone'],
        )

        return Response({'status': 'ok'})

# TODO: update item view


class TelegramEnterCodeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        """User enter the code he received. Thus it init session for auto operations."""
        qs = get_user_model().objects.all()
        user = qs.select_related('telegram_profile').get(id=request.user.id)

        serializer = TelegramEnterCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        _code = validated_data['code']

        if not hasattr(user, 'telegram_profile'):
            raise ValidationError(USER_TG_CREDS_NOT_EXISTS_ERROR)

        logger.info(f'Send tg code from user to telethon to init sessions for: {user}...')
        posted = post_telegram_code(
            api_key=user.telegram_profile.api_key,
            api_hash=user.telegram_profile.api_hash,
            phone=user.telegram_profile.phone,
            password=validated_data.get('password'),
            code=validated_data['code'],
        )
        logger.info(f'Got {posted}')

        return Response({'status': 'ok'})
