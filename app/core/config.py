import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App Settings
    PROJECT_NAME: str = "AI Recruitment Assistant"

    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "a_very_secret_key_for_local_dev")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # API Keys
    GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY")
    PINECONE_API_KEY: str = os.environ.get("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.environ.get("PINECONE_ENVIRONMENT")


settings = Settings()