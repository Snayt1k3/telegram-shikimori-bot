from pydantic import BaseModel


class Response(BaseModel):
    status: int
    text: dict | list
    additionalInfo: dict | None = None
