from datetime import datetime

from beanie import Document
from pydantic import Field


class ImageRequest(Document):
    user_id: str
    image_url: str
    llm_response: dict
    created_at: datetime = Field(default_factory=datetime.now())

    class Settings:
        name = "image_requests"
