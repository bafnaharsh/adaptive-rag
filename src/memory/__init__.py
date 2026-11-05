from langchain_core.chat_history import BaseChatMessageHistory

from src.core.config import settings


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """MongoDB-backed history when MONGO_URL is set, otherwise in-process memory."""
    if settings.MONGO_URL:
        from src.memory.chat_history_mongo import MongoDBChatMessageHistory

        return MongoDBChatMessageHistory(session_id)
    from src.memory.chathistory_in_memory import get_history

    return get_history(session_id)
