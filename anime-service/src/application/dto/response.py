from typing import Any, TypedDict


class ResponseDTO(TypedDict):
    error: str | None
    data: Any
    status: int
