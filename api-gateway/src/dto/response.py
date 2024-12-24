from pydantic import BaseModel


class ResponseDTO(BaseModel):
    error: str | None
    status: int
    data: dict | list | None
