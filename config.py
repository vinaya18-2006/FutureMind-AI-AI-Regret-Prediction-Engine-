import os
from dotenv import load_dotenv

# Load environment variables from the backend directory .env file
project_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(project_dir, ".env"))

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_API_BASE: str = os.getenv("GEMINI_API_BASE", "https://apidev.navigatelabsai.com")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./capstone.db")
    # Firebase configuration (optional fallback)
    FIREBASE_CREDENTIALS_JSON: str = os.getenv("FIREBASE_CREDENTIALS_JSON", "")

settings = Settings()