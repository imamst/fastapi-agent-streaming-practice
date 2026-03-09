from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.engine import get_db
from app.modules.chats.schema import ChatRequest

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/")
def generate_answer(request: ChatRequest, db_session: Session = Depends(get_db)):
    pass
