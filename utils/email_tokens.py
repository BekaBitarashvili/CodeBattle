from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app


def _serializer(salt):
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=salt)


def generate_verify_token(email):
    return _serializer("email-verify").dumps(email)


def confirm_verify_token(token, max_age=None):
    if max_age is None:
        max_age = current_app.config.get("EMAIL_TOKEN_MAX_AGE", 3600)
    try:
        return _serializer("email-verify").loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


def generate_reset_token(email):
    return _serializer("password-reset").dumps(email)


def confirm_reset_token(token, max_age=None):
    if max_age is None:
        max_age = current_app.config.get("EMAIL_TOKEN_MAX_AGE", 3600)
    try:
        return _serializer("password-reset").loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None