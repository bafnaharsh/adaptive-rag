"""
MongoDB client, created on first use so motor is only needed when MONGO_URL is set.
"""

from functools import lru_cache

from src.core.config import settings


@lru_cache(maxsize=1)
def get_db():
    from motor.motor_asyncio import AsyncIOMotorClient

    return AsyncIOMotorClient(settings.MONGO_URL)["adaptive_rag"]
