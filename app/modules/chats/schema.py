from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: int
    message: str
