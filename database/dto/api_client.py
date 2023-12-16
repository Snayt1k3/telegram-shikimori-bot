from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: int
    text: dict | list
    additionalInfo: dict | None = None


class ShikimoriResponse(BaseResponse):
    pass
