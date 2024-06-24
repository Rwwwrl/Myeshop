from typing import Annotated

from fastapi import Depends

from user_identity_cqrs_contract import hints

from .get_user_from_request import get_user_from_http_request


# TODO возможно нужно переделать в декоратор
def login_required(user_id: Annotated[hints.UserId, Depends(get_user_from_http_request)]) -> None:
    # синтаксический сахар:
    # мне хотелось иметь зависимость, обозначающую, что для запроса пользователь должен быть авторизован.
    # Зависимость `get_user_from_http_request` обеспечивает требование, чтобы пользователь был авторизован,
    # но ее название ненастолько "явное", как `login_required`
    return None
