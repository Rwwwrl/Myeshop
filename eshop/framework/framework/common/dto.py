from pydantic import BaseModel, ConfigDict


class DTO(BaseModel, frozen=True):
    model_config = ConfigDict(extra='forbid')
