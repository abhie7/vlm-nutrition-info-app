import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services import vlm_service
from datetime import datetime
import uuid
from app.database.image_analysis_repository import ImageAnalysisRepository
import traceback

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AnalysisRequest(BaseModel):
    user_uuid: str
    food_name: str
    meal_type: str
    tags: list
    image_url: str


@router.post("/analyze")
async def analyze_image(
    request: Request,
    payload: AnalysisRequest,
):
    request_id = str(uuid.uuid4())

    try:
        start_time = datetime.now()
        llm_response = await vlm_service.get_nutrition_info(payload.image_url)

        if not llm_response:
            raise HTTPException(
                status_code=503,
                detail="Failed to generate response from LLM",
            )

        nutrient_info = json.loads(llm_response["response"])
        processing_time = round((datetime.now() - start_time).total_seconds(), 2)

        # Store result in database
        analysis_repo = ImageAnalysisRepository()
        await analysis_repo.insert_one(
            {
                "user_uuid": payload.user_uuid,
                "food_name": payload.food_name,
                "meal_type": payload.meal_type,
                "request_id": request_id,
                "tags": payload.tags,
                "image_url": payload.image_url,
                "nutrition_info": nutrient_info,
                "token_usage": {
                    "prompt_tokens": llm_response["prompt_tokens"],
                    "completion_tokens": llm_response["completion_tokens"],
                    "total_tokens": llm_response["total_tokens"],
                },
                "created_at": datetime.now(),
                "status": "completed",
                "vlm_response_time": llm_response["completion_time"],
                "processing_time": processing_time,
            }
        )

        return {
            "user_uuid": payload.user_uuid,
            "food_name": payload.food_name,
            "meal_type": payload.meal_type,
            "request_id": request_id,
            "tags": payload.tags,
            "image_url": payload.image_url,
            "nutrition_info": nutrient_info,
            "token_usage": {
                "prompt_tokens": llm_response["prompt_tokens"],
                "completion_tokens": llm_response["completion_tokens"],
                "total_tokens": llm_response["total_tokens"],
            },
            "created_at": datetime.now(),
            "status": "completed",
            "vlm_response_time": llm_response["completion_time"],
            "processing_time": processing_time,
        }

    except Exception as e:
        traceback.print_exc(e)
        raise HTTPException(status_code=500, detail="Internal server error")
