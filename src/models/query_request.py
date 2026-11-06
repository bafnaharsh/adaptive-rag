"""
Query request model.
"""

from typing import Literal

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Request model for RAG queries."""

    query: str
    session_id: str = "default"
    mode: Literal["ladder", "agent"] = "ladder"  # ladder = fixed escalation; agent = the model picks the tools
