from typing import Annotated

from fastapi import Depends, HTTPException, status

from user_identity_cqrs_contract.query.query_response import UserIdWithRoleDTO, UserRoleEnum

from .get_user_from_http_request import get_user_from_http_request


def admin_required(user: Annotated[UserIdWithRoleDTO, Depends(get_user_from_http_request)]) -> None:
    if user.role != UserRoleEnum.ADMIN:
        raise HTTPException(detail='you must be admin', status_code=status.HTTP_403_FORBIDDEN)
