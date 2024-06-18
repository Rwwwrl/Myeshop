from functools import partial
from typing import Dict, Optional, Type, Union, cast

from fastapi import HTTPException, status

from pydantic import BaseModel


class PartializedHttpExceptionProtocol(BaseModel):
    detail: Optional[Union[str, None]] = None
    headers: Optional[Dict[str, str]] = None


BadRequestException = cast(
    Type[PartializedHttpExceptionProtocol],
    partial(HTTPException, status_code=status.HTTP_400_BAD_REQUEST),
)

InternalServerError = cast(
    Type[PartializedHttpExceptionProtocol],
    partial(HTTPException, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
)
