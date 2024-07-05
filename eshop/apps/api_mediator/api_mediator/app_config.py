from typing import List

from fastapi import APIRouter


class ApiMediatorAppConfig:

    name = 'api_mediator'

    @classmethod
    def get_api_routers(cls) -> List[APIRouter]:
        from api_mediator.views.http.basket.api_router import api_router as basket_api_router

        return [
            basket_api_router,
        ]

    @classmethod
    def import_http_views(cls) -> None:
        from api_mediator.views import http    # noqa
