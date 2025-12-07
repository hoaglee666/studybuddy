from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    #app
    APP_NAME: str = "StudyBuddy API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    #db
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/studybuddy"

    #jwt
    SECRET_KEY: str = "iGPz9qufe0-rpv0rOWnCD1fBtF6TcT7flqsd_gfFOPY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    #oauth2 google
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"

    #openai
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    #cors
    CORS_ORIGINS: list = [
        "http://10.0.2.2:8000",  # android emulator
        "http://localhost",
        "http://localhost:65208",
        "http://127.0.0.1",
        "http://192.168.123.2",     # your local network IP
        "http://192.168.123.2:8000",
    ]
    # regex to match localhost with any port (used for dynamic dev ports, e.g. Flutter web)
    CORS_ORIGIN_REGEX: str = r"^http://localhost(:[0-9]+)?$"

    #file upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config: 
        env_file = ".env"
        case_sensitive = True

settings = Settings()