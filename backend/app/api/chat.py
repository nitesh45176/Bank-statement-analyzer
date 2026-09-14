from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from fastapi.responses import StreamingResponse
import json
import traceback
from app.agent.graph import graph
from app.services.statement_store import StatementStore


router = APIRouter()


class ChatRequest(BaseModel):
    statement_id: str
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):
    statement = StatementStore.get(request.statement_id)

    if not statement:
        raise HTTPException(
            status_code=404,
            detail="Statement not found. Please upload your statement first."
        )

    state = {
        "statement_id": request.statement_id,
        "user_query": request.message,
        "messages": [
            HumanMessage(
                content=f"""
Statement ID: {request.statement_id}

Question:
{request.message}
"""
            )
        ],
    }

    try:
        result = graph.invoke(state)
        messages = result["messages"]
        final_message = messages[-1]
        return {
            "answer": final_message.content
        }
    except Exception as e:
        print(f"[chat] Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    statement = StatementStore.get(request.statement_id)

    if not statement:
        raise HTTPException(
            status_code=404,
            detail="Statement not found. Please upload your statement first."
        )

    state = {
        "statement_id": request.statement_id,
        "user_query": request.message,
        "messages": [
            HumanMessage(
                content=f"""
Statement ID: {request.statement_id}

Question:
{request.message}
"""
            )
        ],
    }

    async def event_generator():
        try:
            async for event in graph.astream(
                state,
                stream_mode="updates",
            ):
                for node_name, node_output in event.items():

                    if not node_output:
                        continue

                    messages = node_output.get("messages", [])

                    for message in messages:
                        # Agent decided to call a tool
                        if hasattr(message, "tool_calls") and message.tool_calls:
                            for tool_call in message.tool_calls:
                                tool_name = (
                                    tool_call.get("name")
                                    if isinstance(tool_call, dict)
                                    else getattr(tool_call, "name", "tool")
                                )
                                yield (
                                    "data: "
                                    + json.dumps({
                                        "type": "tool_call",
                                        "tool": tool_name,
                                    })
                                    + "\n\n"
                                )

                        # Tool returned data
                        elif (
                            type(message).__name__.startswith("Tool")
                            or getattr(message, "type", "") == "tool"
                        ):
                            yield (
                                "data: "
                                + json.dumps({
                                    "type": "tool_result",
                                })
                                + "\n\n"
                            )

                        # Final AI response
                        elif (
                            type(message).__name__.startswith("AI")
                            or getattr(message, "type", "") == "ai"
                        ) and message.content:
                            yield (
                                "data: "
                                + json.dumps({
                                    "type": "message",
                                    "content": message.content,
                                })
                                + "\n\n"
                            )

            yield (
                "data: "
                + json.dumps({"type": "done"})
                + "\n\n"
            )

        except Exception as e:
            print(f"[chat_stream] Stream exception: {e}")
            traceback.print_exc()
            yield (
                "data: "
                + json.dumps({
                    "type": "error",
                    "message": str(e),
                })
                + "\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )