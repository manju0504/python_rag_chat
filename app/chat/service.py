import asyncio

from fastapi import APIRouter, WebSocket, HTTPException
from starlette.websockets import WebSocketState

from .agent import RAGAgent
from .history import ChatHistory

router = APIRouter()
chat_history = ChatHistory()


@router.post("/api/chat/start")
async def start_chat(asset_id: str):
    chat_id = await chat_history.create_chat(asset_id)
    return {"chat_id": chat_id}

@router.websocket("/api/chat/message/{chat_id}")
async def chat_message(websocket: WebSocket, chat_id: str):
    await websocket.accept()
    connection_open = True
    try:
        asset_id = await chat_history.get_asset_id(chat_id)
        if not asset_id:
            await websocket.send_text(f"Error: Invalid chat ID {chat_id}")
            return

        agent = RAGAgent(chat_id, asset_id)

        while connection_open:
            message = await websocket.receive_text()
            try:
                response_text = ""
                async for response_chunk in agent.generate_response(message):
                    response_text += response_chunk
                    await websocket.send_text(response_chunk)
                    await asyncio.sleep(0)  # Allow other tasks to run

                await chat_history.add_message(chat_id, message, response_text)
            except Exception as e:
                print(e)  # Log the error
                await websocket.send_text(f"Error: {str(e)}")
    except Exception as e:
        connection_open = False
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close(code=1000, reason=str(e))
    finally:
        if connection_open and websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()


@router.get("/api/chat/history")
async def get_chat_history(chat_id: str):
    history = await chat_history.get_history(chat_id)
    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return history