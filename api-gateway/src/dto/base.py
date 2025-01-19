from pydantic import BaseModel

from src.utils.filter import filter_none_params


class Model(BaseModel):
    def to_dict(self) -> dict:
        return filter_none_params(self.model_dump())
