from fastapi import APIRouter, FastAPI, Depends
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(tags=["endpoints"])


class Endpoint(BaseModel):
    path: str
    method: str
    description: str
    tags: List[str]
    payload: Dict[str, Any] = None


def get_app() -> FastAPI:
    from main import app

    return app


@router.get("/endpoints", response_model=List[Endpoint])
def get_endpoints(app: FastAPI = Depends(get_app)):
    routes = [
        {
            "path": "/analyze",
            "method": "POST",
            "description": "Analyze an image",
            "tags": ["image"],
            "payload": {"image_url": "string"},
        },
        {
            "path": "/token",
            "method": "POST",
            "description": "Get an authentication token",
            "tags": ["auth"],
            "payload": {"username": "string", "password": "string"},
        },
        {
            "path": "/users/me",
            "method": "GET",
            "description": "Get current user information",
            "tags": ["auth"],
            "payload": {},
        },
    ]
    return routes
