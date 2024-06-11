from fastapi import APIRouter


class ApiGatewayAppConfig:

    name = 'api_gateway'

    @classmethod
    def get_api_router(cls) -> APIRouter:
        from .api_router import api_router

        return api_router

    @classmethod
    def import_http_views(cls) -> None:
        raise NotImplementedError

    @classmethod
    def init(cls) -> None:
        cls.import_http_views()
