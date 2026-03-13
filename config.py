from dotenv import load_dotenv
load_dotenv(override=False)

import os
from datetime import timedelta


class Config:
    # ── Security ──────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # ── Database ──────────────────────────────────────
    BASE_DIR      = os.path.abspath(os.path.dirname(__file__))
    _INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(_INSTANCE_DIR, exist_ok=True)

    _db_url = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(_INSTANCE_DIR, 'codemama.db')}"
    )
    # Render-ის postgres:// → postgresql://
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Session ───────────────────────────────────────
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    REMEMBER_COOKIE_DURATION   = timedelta(days=30)

    # ── Brevo HTTP API ────────────────────────────────
    BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")

    # ── Judge0 Code Execution ─────────────────────────
    JUDGE0_URL     = os.environ.get("JUDGE0_URL",     "https://ce.judge0.com")
    JUDGE0_API_KEY = os.environ.get("JUDGE0_API_KEY", "")
    JUDGE0_HOST    = os.environ.get("JUDGE0_HOST",    "ce.judge0.com")

    # ── Token expiry ──────────────────────────────────
    EMAIL_TOKEN_MAX_AGE = 3600

    # ── App-specific ──────────────────────────────────
    LANGUAGES        = ["ka", "en"]
    DEFAULT_LANGUAGE = "ka"
    XP_PER_EASY      = 30
    XP_PER_MEDIUM    = 80
    XP_PER_HARD      = 150
    STREAK_BONUS_XP  = 10


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False