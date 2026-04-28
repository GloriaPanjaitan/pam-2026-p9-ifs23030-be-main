import os
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

class Config:
    # Port aplikasi, default ke 5000 jika tidak disetting di .env
    APP_PORT = int(os.getenv("APP_PORT", 5000))

    # Token API Gemini (menggunakan nama variabel yang konsisten dengan llm_service)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Konfigurasi Database
    # Kita arahkan ke data.db agar rapi
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Opsi tambahan jika ingin menggunakan URL base khusus untuk LLM (opsional)
    BASE_URL = os.getenv("LLM_BASE_URL")