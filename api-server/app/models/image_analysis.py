from pydantic import BaseModel
from beanie import Document


class ImageAnalysisBase(BaseModel):
    image_url: str
    user_uuid: str


class ImageAnalysisCreate(ImageAnalysisBase):
    pass


class ImageAnalysis(Document):
    image_url: str

    class Settings:
        collection = "image_analysis"
