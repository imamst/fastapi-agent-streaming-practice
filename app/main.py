from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from app.modules.chats.router import chat_router
from app.modules.sessions.router import session_router

BASE_DIR = Path(__file__).resolve().parents[1]
CHAT_HTML_PATH = BASE_DIR / "app" / "static" / "chat.html"


app = FastAPI()

app.include_router(session_router)
app.include_router(chat_router)


@app.get("/", response_class=HTMLResponse)
async def chat_form():
    return HTMLResponse(content=CHAT_HTML_PATH.read_text(encoding="utf-8"))


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
    )
