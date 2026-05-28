from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://gvevent:password@localhost:5432/guestvision"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "your_secret_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # InsightFace
    INSIGHTFACE_MODEL: str = "buffalo_l"
    INSIGHTFACE_MODEL_DIR: str = "/opt/models"
    FACE_THRESHOLD: float = 0.45
    FACE_QUALITY_MIN: float = 0.5
    
    # Storage
    STORAGE_MODE: str = "local"
    LOCAL_STORAGE_PATH: str = "/opt/guestvision/uploads"
    AWS_BUCKET: Optional[str] = None
    AWS_REGION: Optional[str] = None
    
    # App
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    DEVICE_SECRET: str = "device_secret_token"
    LOAD_FACE_ENGINE_ON_STARTUP: bool = True
    INIT_DB_ON_STARTUP: bool = True
    STRICT_AI_STARTUP: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
