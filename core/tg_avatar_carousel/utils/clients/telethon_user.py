from typing import Optional

import requests

# TODO: to settings
API_ENDPOINT = "http://telethon_user:8000"


def request_telegram_code(api_key: str, api_hash: str, phone: str):
    return requests.post(
        API_ENDPOINT + '/api/v1/request-code',
        json={'phone': phone, 'api_key': api_key, 'api_hash': api_hash},
    ).json()


def post_telegram_code(api_key: str, api_hash: str, phone: str, code: str, password: Optional[str]):
    posted = requests.post(
        API_ENDPOINT + '/api/v1/post-code',
        json={'phone': phone, 'api_key': api_key, 'api_hash': api_hash, 'code': code, 'password': password},
    )
    if not posted.status_code == 200:
        # TODO: special exception
        raise Exception(f'status code from telethon client is not 200, got {posted.content}')

    return posted.json()


def post_change_avatar(api_key: str, api_hash: str, phone: str, image_url: str):
    posted = requests.post(
        API_ENDPOINT + '/api/v1/change-avatar',
        json={'phone': phone, 'api_key': api_key, 'api_hash': api_hash, 'image_url': image_url},
    )
    if not posted.status_code == 200:
        # TODO: special exception
        raise Exception(f'status code from telethon client is not 200, got {posted.content}')

    return posted.json()
