from pydantic import BaseModel


class JobStatus(BaseModel):
    success: bool
    error: str | None
