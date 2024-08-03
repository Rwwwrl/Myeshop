from pydantic import BaseModel, ConfigDict


class IContext(BaseModel, frozen=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
