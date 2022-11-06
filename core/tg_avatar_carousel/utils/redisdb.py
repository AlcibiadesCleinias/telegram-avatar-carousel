from redis import Redis

from django.conf import settings

redis = Redis(settings.REDIS_HOST, settings.REDIS_PORT, decode_responses=True)

def redis_key_to_current_image(user_id):
    return f'{user_id}:current_image'
