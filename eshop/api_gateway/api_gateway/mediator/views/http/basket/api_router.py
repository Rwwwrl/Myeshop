from fastapi import APIRouter

from api_gateway.base_api_router import base_api_router

api_router = APIRouter(
    prefix=f'{base_api_router.prefix}/basket',
    tags=[f'{base_api_router.tags[0]}/basket/'],
)
