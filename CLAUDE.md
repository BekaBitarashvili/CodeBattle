# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CodeBattle (also called "CodeMama") is a Georgian educational coding competition platform built with Flask. It supports bilingual content (Georgian + English), real-time code execution via the Judge0 API, gamification (XP, badges, streaks), user authentication with email verification, and olympiad (tournament) management.

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
flask run

# Run with Gunicorn (production)
gunicorn wsgi:app
```

Required environment variables (see `.env.example`):
- `SECRET_KEY` — Flask session secret
- `DATABASE_URL` — SQLite (default: `sqlite:///instance/codemama.db`) or PostgreSQL
- `JUDGE0_URL` — Code execution endpoint (default: `https://ce.judge0.com`)
- `ADMIN_EMAILS` — Comma-separated list of admin email addresses
- `BREVO_API_KEY` — Email service (optional; dev mode prints links to console)

## Database

Uses Flask-Migrate (Alembic). The database auto-seeds badges and news on first run.

```bash
flask db migrate -m "message"   # Create a new migration
flask db upgrade                 # Apply pending migrations
```

SQLite for development, PostgreSQL for production (Render.com). The app automatically converts `postgres://` → `postgresql://` URLs.

## Architecture

**Entry point**: `app.py` — `create_app()` factory registers blueprints and seeds initial data.

**Blueprints** (`routes/`): `main`, `auth`, `tasks`, `ratings`, `olympiad`, `dashboard`, `admin`, `about`, `help`.

**Models** (`models.py`): `User`, `Task`, `Submission`, `Badge`, `News`, `Olympiad`, `OlympiadRegistration`.

**Utils** (`utils/`):
- `judge.py` — Submits code to Judge0, polls for result, compares output against test cases
- `send_email.py` — Brevo SMTP integration
- `email_tokens.py` — Token generation for email verification

**Templates** (`templates/`): Jinja2 with a `base.html` master layout. All content uses a `t()` context processor function for bilingual (ka/en) rendering.

**Bilingual pattern**: All content models (tasks, news, etc.) have `_ka` and `_en` field variants. The `t()` function selects based on the user's session language.

## Key Design Decisions

- **Admin access** is email-based via the `ADMIN_EMAILS` env var — no role column in the DB.
- **Test cases** are stored as JSON on the `Task` model.
- **XP system**: Easy=30, Medium=80, Hard=150 XP per first solve; 10 XP streak bonus; 500 XP per level.
- **Judge0** is used as a free public API (no auth key required by default).
- **Email verification** is required before login.

## Deployment

Deployed to Render.com. The `wsgi.py` file is the WSGI entry point for Gunicorn.
