from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str
    LLM_API_KEY: str
    LLM_MODEL: str = "llama-3.2-11b-vision-preview"
    LOG_FILE: str = "app/logs/api_logs.jsonl"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize settings only once
settings = Settings()
