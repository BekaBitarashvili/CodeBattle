import os
from datetime import timedelta


class Config:
    # ── Security ──────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # ── Database ──────────────────────────────────────
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Auto-create instance/ folder so SQLite never fails on first run
    _INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(_INSTANCE_DIR, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(_INSTANCE_DIR, 'codemama.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Session ───────────────────────────────────────
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    REMEMBER_COOKIE_DURATION   = timedelta(days=30)

    # ── App-specific ──────────────────────────────────
    LANGUAGES         = ["ka", "en"]
    DEFAULT_LANGUAGE  = "ka"
    XP_PER_EASY       = 30
    XP_PER_MEDIUM     = 80
    XP_PER_HARD       = 150
    STREAK_BONUS_XP   = 10   # bonus XP per streak day


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Override SECRET_KEY from environment in production!