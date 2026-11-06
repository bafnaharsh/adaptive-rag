"""
Main FastAPI application entry point: the API under /rag and the chat UI (web/) at /.
"""

import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes import router
from src.core.config import ROOT
from src.llms import llm
from src.rag import store


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Warm up in the background so the first question does not pay the LLM session start and model loading.
    llm.warm()
    threading.Thread(target=store.warm, daemon=True).start()
    yield


app = FastAPI(title="Adaptive RAG API", lifespan=lifespan)
app.include_router(router)
app.mount("/", StaticFiles(directory=ROOT / "web", html=True, check_dir=False), name="ui")  # last: API routes win
