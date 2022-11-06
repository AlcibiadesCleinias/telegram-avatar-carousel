# TODO: simplify apis and use logic.py
import logging

from fastapi import APIRouter, HTTPException
from telethon.errors import SessionPasswordNeededError

import schemas
from config.misc import redis
from telegram.change_avatar import change_avatar
from telegram.client import get_telegram_client

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post('/request-code', response_model=schemas.RequestCode)
async def request_code(request_code: schemas.RequestCode):
    client = await get_telegram_client(
        api_key=request_code.api_key,
        api_hash=request_code.api_hash,
        phone=request_code.phone,
    )

    if not await client.is_user_authorized():
        sent = await client.send_code_request(request_code.phone)
        logger.info(f'Send request for the code, got: {sent}')

        logger.info('Try to save code hash into redis...')
        await redis.set(request_code.phone, sent.phone_code_hash)
    return request_code


@router.post('/post-code', response_model=schemas.PostCodeOut)
async def post_code(post_code: schemas.PostCodeIn):
    client = await get_telegram_client(
        api_key=post_code.api_key,
        api_hash=post_code.api_hash,
        phone=post_code.phone,
    )

    phone_code_hash = await redis.get(post_code.phone)
    logger.info('Phone code hash %s', phone_code_hash)
    if not phone_code_hash:
        raise HTTPException(
            status_code=400,
            detail="No phone code hash - means you have not requested code yet.",
        )
    try:
        signed = await client.sign_in(
            phone=post_code.phone,
            code=post_code.code,
            phone_code_hash=phone_code_hash,
        )
    except SessionPasswordNeededError:
        signed = await client.sign_in(
            password=post_code.password,
        )
    finally:
        await client.disconnect()
    logger.info(f'Tried to sign with code and {phone_code_hash = }, got {signed}')
    return post_code


@router.post('/change-avatar', response_model=schemas.ChangeAvatar)
async def _change_avatar(change_avatar_in: schemas.ChangeAvatar):
    client = await get_telegram_client(
        api_key=change_avatar_in.api_key,
        api_hash=change_avatar_in.api_hash,
        phone=change_avatar_in.phone,
    )
    logger.info('Change avatar for %s...', change_avatar_in.phone)
    await change_avatar(client, change_avatar_in.image_url)
    return change_avatar_in
