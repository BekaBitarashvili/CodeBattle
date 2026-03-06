import os
from datetime import timedelta

# https://myaccount.google.com/apppasswords
class Config:
    # ── Security ──────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # ── Database ──────────────────────────────────────
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
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

    # ── Flask-Mail (Gmail SMTP) ───────────────────────
    MAIL_SERVER   = "smtp.gmail.com"
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "codemama@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "kmzlrxhabaxiwhog")   # Gmail App Password აქ
    MAIL_DEFAULT_SENDER = ("CodeMama", os.environ.get("MAIL_USERNAME", "codemama@gmail.com"))

    # ── Token expiry ──────────────────────────────────
    EMAIL_TOKEN_MAX_AGE = 3600   # 1 საათი (წამებში)

    # ── App-specific ──────────────────────────────────
    LANGUAGES         = ["ka", "en"]
    DEFAULT_LANGUAGE  = "ka"
    XP_PER_EASY       = 30
    XP_PER_MEDIUM     = 80
    XP_PER_HARD       = 150
    STREAK_BONUS_XP   = 10


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False