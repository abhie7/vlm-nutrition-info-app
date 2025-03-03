from pydantic import BaseModel
from beanie import Document


class ImageAnalysisBase(BaseModel):
    image_url: str
    user_id: str


class ImageAnalysisCreate(ImageAnalysisBase):
    pass


class ImageAnalysis(Document):
    image_url: str
    analysis_result: dict

    class Settings:
        collection = "image_analysis"
