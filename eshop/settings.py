from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
from typing import List, Type

import decouple

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

import pydantic

from sqlalchemy import URL
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase as SqlalchemyDeclarativeBase

from eshop.apps.test_app.app_config import TestAppConfig

from framework.fastapi.app_config import IAppConfig

from user_identity.app_config import UserIdentityAppConfig

INSTALLED_APPS: List[Type[IAppConfig]] = [
    TestAppConfig,
    UserIdentityAppConfig,
]


def init_logging() -> None:
    from logging import config

    logs_dir = BASE_DIR / 'logs'
    logs_dir.mkdir(exist_ok=True)
    config.dictConfig(LOGGING_CONFIG)


def import_all_models_in_project() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_models()


def import_http_views() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_http_views()


def include_routes() -> None:
    for app_config in INSTALLED_APPS:
        MAIN_APP.include_router(app_config.get_api_router())


def import_cqrs_controllers() -> None:
    for app_config in INSTALLED_APPS:
        app_config.import_cqrs_handlers()


@asynccontextmanager
async def lifespan(app: FastAPI):
    import_http_views()
    include_routes()
    import_cqrs_controllers()
    init_logging()
    yield


MAIN_APP = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseSettings(pydantic.BaseModel, frozen=True):
    pass


class DatabaseSettings(BaseSettings):

    name: str = decouple.config('DB_NAME')
    host: str = decouple.config('DB_HOST')
    login: str = decouple.config('DB_USER_LOGIN')
    password: str = decouple.config('DB_USER_PASSWORD')


class UserIdentityServiceSettings(BaseSettings):

    secret: str = decouple.config('USER_IDENTITY_SERVICE_SECRET')
    token_life_time_duration: timedelta = timedelta(minutes=5)


class Settings(BaseSettings):

    db: DatabaseSettings = DatabaseSettings()
    user_identity_service_settings: UserIdentityServiceSettings = UserIdentityServiceSettings()


SETTINGS = Settings()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':
        {
            'default_formatter': {
                'format': '%(asctime)s:[%(levelname)s] %(message)s',
            },
            'json':
                {
                    '()':
                        "pythonjsonlogger.jsonlogger.JsonFormatter",
                    'format':
                        "%(asctime)s %(levelname)s %(name)s %(pathname)s %(lineno)s %(funcName)s %(message)s %(extra)s %(exc_info)s",    # noqa
                },
        },
    'handlers':
        {
            'stream_handler': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default_formatter',
            },
            'json_stream_handler': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
            'json_rotatating_file_handler':
                {
                    'level': 'WARNING',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'logs/logs.jsonl',
                    'maxBytes': 1000,
                    'backupCount': 0,
                    'formatter': 'json',
                },
        },
    'loggers':
        {
            '':
                {
                    'handlers': [
                        'json_stream_handler',
                        'json_rotatating_file_handler',
                    ],
                    'level': 'DEBUG',
                    'propagate': True,
                },
        },
}

DB_URL = URL.create(
    drivername='postgresql',
    database=SETTINGS.db.name,
    host=SETTINGS.db.host,
    username=SETTINGS.db.login,
    password=SETTINGS.db.password,
)


class SQLALCHEMY_BASE(SqlalchemyDeclarativeBase):
    pass


SQLALCHEMY_ENGINE = create_engine(url=DB_URL)

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='user_identity/token/')
