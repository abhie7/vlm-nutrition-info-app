from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str
    API_KEY: str
    MODEL: str = "llama-3.2-11b-vision-preview"
    LOG_FILE: str = "logs/api_logs.jsonl"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize settings only once
settings = Settings()
