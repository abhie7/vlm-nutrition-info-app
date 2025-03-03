from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.vlm_service import VLMService
from datetime import datetime
import uuid
from app.database.image_analysis_repository import ImageAnalysisRepository

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AnalysisRequest(BaseModel):
    image_url: str


@router.post("/analyze", dependencies=[Depends(oauth2_scheme)])
async def analyze_image(
    request: Request,
    image_url: AnalysisRequest,
    token: str = Depends(oauth2_scheme),
):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id  # Store request_id in request state

    # Log analysis start with detailed metadata
    request.state.logger.info(
        "Starting image analysis",
        extra={
            "request_id": request_id,
            "image_url": image_url.image_url,
            "user_id": request.state.user_id,
            "method": "analyze_image",
        },
    )

    try:
        start_time = datetime.now()
        llm_response = await VLMService.generate_response(image_url.image_url)

        if not llm_response:
            request.state.logger.error(
                "LLM response was empty",
                extra={"request_id": request_id, "image_url": image_url.image_url},
            )
            raise HTTPException(
                status_code=503,
                detail="Failed to generate response from LLM",
            )

        # Store result in database
        analysis_repo = ImageAnalysisRepository()
        await analysis_repo.insert_one(
            {
                "request_id": request_id,
                "image_url": image_url.image_url,
                "result": llm_response,
                "created_at": datetime.now(),
                "status": "completed",
                "processing_time": (datetime.now() - start_time).total_seconds(),
            }
        )

        request.state.logger.info(
            "Analysis completed successfully",
            extra={
                "request_id": request_id,
                "processing_time": (datetime.now() - start_time).total_seconds(),
            },
        )

        return {"result": llm_response}

    except Exception as e:
        request.state.logger.error(
            f"Analysis failed: {str(e)}",
            extra={
                "request_id": request_id,
                "image_url": image_url.image_url,
                "error_type": type(e).__name__,
            },
        )
        raise HTTPException(status_code=500, detail="Internal server error")
