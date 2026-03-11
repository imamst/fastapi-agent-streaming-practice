import json

from agents import Agent, RawResponsesStreamEvent, RunItemStreamEvent, Runner
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from openai.types.responses import ResponseFunctionToolCall, ResponseTextDeltaEvent
from sqlmodel import Session

from app.models.engine import get_db
from app.modules.agents.models import llm_model
from app.modules.agents.prompt import SYSTEM_PROMPT
from app.modules.agents.tools import search_web
from app.modules.chats.schema import ChatRequest

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/")
async def generate_answer(request: ChatRequest, db_session: Session = Depends(get_db)):
    agent = Agent(
        "Assistant", instructions=SYSTEM_PROMPT, model=llm_model, tools=[search_web]
    )
    runner = Runner.run_streamed(agent, request.message)

    async def event_generator():
        async for event in runner.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event, RawResponsesStreamEvent
            ):
                if isinstance(event.data, ResponseTextDeltaEvent):
                    yield f"data: {json.dumps({'type': 'text', 'content': event.data.delta})} \n\n" #noqa

            elif isinstance(event, RunItemStreamEvent) and event.name == "tool_called":
                if isinstance(event.item.raw_item, ResponseFunctionToolCall):
                    yield f"data: {json.dumps({'type': 'tool_call', 'tool_name': event.item.raw_item.name, "arguments": event.item.raw_item.arguments})} \n\n" #noqa

    return StreamingResponse(event_generator(), media_type="text/event-stream")
