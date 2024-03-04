from pydantic import BaseModel


class DTO(BaseModel, frozen=True):
    pass
