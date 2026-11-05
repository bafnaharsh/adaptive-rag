"""
Settings from environment variables (and a .env file at the repo root).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


class Settings:
    """Application settings loaded from environment variables."""

    # Comma-separated fallback chain. cli:<name> runs a harness CLI you are logged into (no API key):
    # cli:claude | cli:agy | cli:copilot. Anything else is BYOK through LangChain's init_chat_model,
    # e.g. openai:gpt-4o-mini, anthropic:claude-sonnet-4-5, google_genai:gemini-2.5-flash, ollama:llama3.1.
    LLM_MODEL: str = os.getenv("LLM_MODEL", "cli:claude")
    # Model flag for cli:* backends; empty = per-CLI default in src/llms/llm.py.
    CLI_MODEL: str = os.getenv("CLI_MODEL", "")
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "180"))

    DATA_DIR: Path = Path(os.getenv("DATA_DIR", ROOT / "data"))
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    RERANK_MODEL: str = os.getenv("RERANK_MODEL", "Xenova/ms-marco-MiniLM-L-6-v2")

    # Web search: Tavily when a key is set, otherwise DuckDuckGo (no key).
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    # Chat history: MongoDB when set, otherwise in-process memory.
    MONGO_URL: str = os.getenv("MONGO_URL", "")


settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
