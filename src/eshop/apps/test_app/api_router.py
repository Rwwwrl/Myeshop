from fastapi import APIRouter

api_router = APIRouter(
    prefix='/test_app',
    tags=[
        'test_app',
    ],
)
