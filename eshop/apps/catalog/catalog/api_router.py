from fastapi import APIRouter

from .app_config import CatalogAppConfig

api_router = APIRouter(
    prefix=f'/{CatalogAppConfig.name}',
    tags=[
        CatalogAppConfig.name,
    ],
)
