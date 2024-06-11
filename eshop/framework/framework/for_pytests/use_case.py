from pydantic import BaseModel, ConfigDict


class UseCase(BaseModel, frozen=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
