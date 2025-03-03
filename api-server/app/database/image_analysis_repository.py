from app.database.base_repository import BaseRepository
from app.models.image_analysis import ImageAnalysis, ImageAnalysisCreate
from datetime import datetime


class ImageAnalysisRepository(BaseRepository):
    def __init__(self):
        super().__init__("image_analyses")

    async def create_analysis(self, analysis: ImageAnalysisCreate):
        analysis_dict = analysis.dict()
        analysis_dict["status"] = "pending"
        analysis_dict["created_at"] = datetime.now()

        result = await self.insert_one(analysis_dict)
        return await self.find_one({"_id": result.inserted_id})

    async def update_result(self, analysis_id: str, result: dict):
        update_result = await self.update_one(
            {"_id": analysis_id},
            {
                "$set": {
                    "result": result,
                    "status": "completed",
                    "completed_at": datetime.now(),
                }
            },
        )
        return update_result.modified_count
