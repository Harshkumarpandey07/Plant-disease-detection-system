
# ============================================================
#  PhytoSense — Configuration
#  backend/config.py
# ============================================================

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ── Core ───────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "phytosense-dev-secret-change-in-production")
    DEBUG      = os.environ.get("DEBUG", "True") == "True"

    # ── Database ───────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'phytosense.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── JWT ────────────────────────────────────────────────
    JWT_SECRET_KEY            = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta(hours=12)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # ── File Upload ────────────────────────────────────────
    UPLOAD_FOLDER      = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}

    # ── ML Model ───────────────────────────────────────────
    MODEL_PATH       = os.path.join(BASE_DIR, "..", "model", "plant_cnn.h5")
    CLASS_NAMES_PATH = os.path.join(BASE_DIR, "..", "model", "class_names.json")
    IMG_SIZE         = (224, 224)

    # ── External APIs ──────────────────────────────────────
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_KEY_HERE")
    OPENWEATHER_BASE    = "https://api.openweathermap.org/data/2.5"


class ProductionConfig(Config):
    DEBUG                   = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY              = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY          = os.environ.get("JWT_SECRET_KEY")
