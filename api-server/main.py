import logging

from app.database.base_repository import init_db
from app.middlewares.logging_middleware import LoggingMiddleware
from app.routes.auth import router as auth_router
from app.routes.endpoints import router as endpoints_router
from app.routes.image import router as image_router
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Configure root logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize logging before database
    logging.info("[VLM-API Server] Initializing logging system...")

    # Initialize database
    await init_db()
    logging.info("[VLM-API Server] Database connection established")

    # Yield control to FastVLM-API
    yield

    # Shutdown sequence
    logging.info("[VLM-API Server] Shutting down VLM-API Server...")


logging.info("[VLM-API Server] Shutdown completed")


app = FastAPI(
    title="VLM-API",
    description="API for analyzing nutritional labels from images",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
origins = ["*", "http://localhost", "http://localhost:3000"]  # allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Add routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(image_router, prefix="/api", tags=["analysis"])
app.include_router(endpoints_router, prefix="/api", tags=["endpoints"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
