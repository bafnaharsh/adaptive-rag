"""
LangGraph state of the escalation ladder in src/rag/graph_builder.py.
"""

import operator
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage

from src.models.evidence import Chunk


class State(TypedDict, total=False):
    """One user turn moving through plan -> rag -> hybrid -> web -> generate <-> verify."""

    question: str                # the user's message as typed
    history: list[BaseMessage]   # earlier turns, for follow-up questions
    standalone: str              # the question rewritten by the planner to stand alone
    route: str                   # planner's choice: knowledge | documents | web
    tier: str                    # deepest tier that ran: knowledge | rag | hybrid | web
    evidence: list[Chunk]        # merged across tiers, best first
    sufficient: bool             # the judge's verdict on the evidence so far
    answered: bool               # the judge also wrote the answer (sufficient evidence): skip generate
    doc_queries: list[str]       # the judge's queries for missing parts the documents likely cover (Tier 2)
    web_queries: list[str]       # the judge's queries for missing parts only the web has (Tier 3)
    answer: str
    citations: list[dict]        # generate's citations, replaced by citations.verify() output
    feedback: str                # verification failures sent back to generate; "" when done
    attempts: int                # generate calls so far
    verified: bool
    trace: Annotated[list[str], operator.add]  # human-readable steps; every node appends
    step: dict                   # the last node's structured step, streamed to the UI by stream_answer()
