from typing import Any, Dict, Optional

from app.config.settings import settings
from app.models.image_analysis import ImageAnalysis
from app.models.user import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)  # Corrected attribute name
    database = client.vlm_image_api
    await init_beanie(database=database, document_models=[User, ImageAnalysis])


class BaseRepository:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    @property
    def collection(self):
        return self.app.database[self.collection_name]

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
