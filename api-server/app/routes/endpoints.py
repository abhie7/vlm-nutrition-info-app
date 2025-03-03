from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter(tags=["endpoints"])


class Endpoint(BaseModel):
    path: str
    method: str
    description: str
    tags: List[str]


@router.get("/endpoints", response_model=List[Endpoint])
def get_endpoints():
    routes = []
    for route in router.application.routes:
        if hasattr(route, "methods"):
            for method in route.methods:
                routes.append(
                    {
                        "path": route.path,
                        "method": method,
                        "description": route.description or "",
                        "tags": route.tags or [],
                    }
                )
    return routes
