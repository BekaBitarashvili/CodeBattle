"""
Token generation and verification using itsdangerous.

Tokens:
  - verify:   email ვერიფიკაციისთვის (ძველი DB-ში წინასწარ შენახული user-ისთვის)
  - register: ახალი user-ის მონაცემები (email, username, pw_hash) token-შია
  - reset:    პაროლის აღდგენისთვის
"""
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app


def _serializer(salt: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=salt)


# ── REGISTER TOKEN (მონაცემები token-შია, DB-ში არ ჩაიწერება) ──

def generate_register_token(email: str, username: str, pw_hash: str) -> str:
    s = _serializer("register-account")
    return s.dumps({"e": email, "u": username, "p": pw_hash})


def confirm_register_token(token: str, max_age: int = 3600):
    """
    Returns (email, username, pw_hash) ან None თუ ვადა ამოიწურა/არასწორია.
    """
    s = _serializer("register-account")
    try:
        data = s.loads(token, max_age=max_age)
        return data["e"], data["u"], data["p"]
    except (BadSignature, SignatureExpired, KeyError):
        return None


# ── VERIFY TOKEN (უკვე DB-ში მყოფი user-ისთვის) ──

def generate_verify_token(email: str) -> str:
    s = _serializer("email-verify")
    return s.dumps(email)


def confirm_verify_token(token: str, max_age: int = 3600):
    """Returns email ან None."""
    s = _serializer("email-verify")
    try:
        return s.loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


# ── RESET TOKEN ──

def generate_reset_token(email: str) -> str:
    s = _serializer("password-reset")
    return s.dumps(email)


def confirm_reset_token(token: str, max_age: int = 3600):
    """Returns email ან None."""
    s = _serializer("password-reset")
    try:
        return s.loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None