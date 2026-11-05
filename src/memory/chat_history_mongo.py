"""
Chat history stored in MongoDB (async only, used when MONGO_URL is set).
"""

from datetime import datetime, timezone
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, message_to_dict

from src.db.mongo_client import get_db


class MongoDBChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.collection = get_db()["chat_history"]

    async def aget_messages(self) -> list[BaseMessage]:
        cursor = self.collection.find({"session_id": self.session_id}).sort("timestamp", 1)
        return messages_from_dict([d["message"] for d in await cursor.to_list(length=None)])

    async def aadd_messages(self, messages: Sequence[BaseMessage]) -> None:
        now = datetime.now(timezone.utc)
        await self.collection.insert_many(
            [{"session_id": self.session_id, "message": message_to_dict(m), "timestamp": now} for m in messages]
        )

    async def aclear(self) -> None:
        await self.collection.delete_many({"session_id": self.session_id})

    def clear(self) -> None:
        raise NotImplementedError("MongoDB history is async only; use aclear()")
