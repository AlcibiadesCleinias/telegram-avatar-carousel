import logging

from rest_framework import serializers

from tg_avatar_carousel.telegram_avatars.models import TelegramProfile

logger = logging.getLogger(__name__)


class TelegramProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramProfile
        fields = ('api_key', 'api_hash', 'phone',)

    def create(self, validated_data):
        _user = self.context["request"].user
        instance = TelegramProfile.objects.create(**validated_data, user=_user)
        return instance


class TelegramRequestCodeSerializer(serializers.Serializer):
    api_key = serializers.CharField()
    api_hash = serializers.CharField()
    phone = serializers.CharField()


class TelegramEnterCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    password = serializers.CharField(required=False, allow_blank=True)
