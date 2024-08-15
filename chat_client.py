import asyncio
import websockets
import json

async def send_message(chat_id, message):
    uri = f"ws://localhost:8000/api/chat/message/{chat_id}"  # Change this to your WebSocket URL
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        full_response = ""
        while True:
            response = await websocket.recv()
            response_data = json.loads(response)
            full_response += response_data["response"]
            print(response_data["response"], end = '', flush=True)
            if response_data.get("done", False):
                break
        return full_response
async def chat():

    chat_id = "YOUR_CHAT_ID"  # Change this to your chat ID
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break
        await send_message(chat_id, message)


asyncio.get_event_loop().run_until_complete(chat())