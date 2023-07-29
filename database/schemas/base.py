from pydantic import BaseModel


class Base(BaseModel):
    chat_id: int = None
