from fastapi import APIRouter

from api.endpoints import router


api_router = APIRouter()
api_router.include_router(router, prefix='', tags=['telegram-auth'])
