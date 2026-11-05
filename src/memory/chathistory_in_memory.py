"""
In-memory chat history (default; lost on restart).
"""

from langchain_core.chat_history import InMemoryChatMessageHistory

_store: dict[str, InMemoryChatMessageHistory] = {}


def get_history(session_id: str) -> InMemoryChatMessageHistory:
    return _store.setdefault(session_id, InMemoryChatMessageHistory())
