import os
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import current_user, login_required
from extensions import db
from models import Olympiad, OlympiadRegistration, User
from functools import wraps

admin_bp = Blueprint("admin", __name__)


# ── Admin check ───────────────────────────────
def is_admin_user(user) -> bool:
    admin_emails = os.environ.get("ADMIN_EMAILS", "")
    allowed = [e.strip().lower() for e in admin_emails.split(",") if e.strip()]
    return user.email.lower() in allowed


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if not is_admin_user(current_user):
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ─────────────────────────────────
@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    olympiads   = Olympiad.query.order_by(Olympiad.start_date.desc()).all()
    total_users = User.query.count()
    total_regs  = OlympiadRegistration.query.count()
    return render_template("admin/dashboard.html",
                           olympiads=olympiads,
                           total_users=total_users,
                           total_regs=total_regs)


# ── Olympiad registrants ──────────────────────
@admin_bp.route("/olympiad/<int:olympiad_id>")
@login_required
@admin_required
def olympiad_registrants(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    regs = (
        OlympiadRegistration.query
        .filter_by(olympiad_id=olympiad_id)
        .join(User)
        .order_by(OlympiadRegistration.registered_at.asc())
        .all()
    )
    return render_template("admin/registrants.html", olympiad=olympiad, regs=regs)


# ── Users list ────────────────────────────────
@admin_bp.route("/users")
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)
