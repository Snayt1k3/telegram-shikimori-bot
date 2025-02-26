from pydantic import BaseModel


class ResponseDTO(BaseModel):
    data: dict | list | None
    error: str | None
    status: int
