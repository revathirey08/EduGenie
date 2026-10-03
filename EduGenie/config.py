import os
from pathlib import Path

from dotenv import load_dotenv


# Find the .env file in the same folder as this config.py
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Load .env
load_dotenv(dotenv_path=ENV_FILE)


# Application settings
APP_NAME = os.getenv("APP_NAME", "EduGenie")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"


# Gemini settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash",
)


def validate_configuration():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add it to the .env file."
        )