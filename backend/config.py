"""
Backend Configuration for MARK 12
Reads settings from environment variables or .env file.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "MARK 12")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "quantum_jarvis_secret_key_2026")

    # Storage paths
    STORAGE_DIR: Path = BASE_DIR / "storage"
    UPLOAD_DIR: Path = BASE_DIR / "storage" / "uploads"
    AUDIO_DIR: Path = BASE_DIR / "storage" / "audio"
    IMAGE_DIR: Path = BASE_DIR / "storage" / "images"
    DOC_DIR: Path = BASE_DIR / "storage" / "documents"

settings = Settings()
