import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 