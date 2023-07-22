from pydantic import BaseModel


class ErrorBase(BaseModel):
    text: str = ''
    code: int = None


class ShikimoriError(ErrorBase):
    pass


class AnilibriaError(ErrorBase):
    pass


class DataBaseError(ErrorBase):
    pass
