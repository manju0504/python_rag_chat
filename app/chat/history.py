import uuid
from typing import List, Dict


class ChatHistory:
    def __init__(self):
        self.chats: Dict[str, Dict] = {}

    async def create_chat(self, asset_id: str) -> str:
        chat_id = str(uuid.uuid4())
        self.chats[chat_id] = {"asset_id": asset_id, "messages": []}
        return chat_id

    async def add_message(self, chat_id: str, user_message: str, bot_response: str):
        if chat_id not in self.chats:
            raise ValueError("Chat ID not found")
        self.chats[chat_id]["messages"].append({"user": user_message, "bot": bot_response})

    async def get_history(self, chat_id: str) -> List[Dict]:
        if chat_id not in self.chats:
            return None
        return self.chats[chat_id]["messages"]

    async def get_asset_id(self, chat_id: str) -> str:
        if chat_id not in self.chats:
            return None
        return self.chats[chat_id]["asset_id"]
