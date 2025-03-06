from typing import Any, Dict, Optional

from app.config.settings import settings
from app.models.image_analysis import ImageAnalysis
from app.models.user import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    database = client.vlm_nutrition_db
    await init_beanie(database=database, document_models=[User, ImageAnalysis])


class BaseRepository:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.collection: AsyncIOMotorCollection = AsyncIOMotorClient(
            settings.MONGODB_URI
        )[settings.MONGODB_DB_NAME][collection_name]

    async def insert_one(self, document: Dict[str, Any]) -> Optional[str]:
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)

    async def find_one(self, filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one(filter)

    async def update_one(self, filter: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = await self.collection.update_one(filter, update)
        return result.modified_count

    async def delete_one(self, filter: Dict[str, Any]) -> int:
        result = await self.collection.delete_one(filter)
        return result.deleted_count
