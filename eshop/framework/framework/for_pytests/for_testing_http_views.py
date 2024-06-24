from pydantic import BaseModel


class ExpectedHttpResponse(BaseModel, frozen=True):

    status_code: int
    body: bytes


class ExpectedHttpResponseException(BaseModel, frozen=True):

    status_code: int
    detail: str
