from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from extensions import db
from models import Olympiad, OlympiadRegistration, User
from functools import wraps

admin_bp = Blueprint("admin", __name__)

# ── Simple password guard ─────────────────────
ADMIN_PASSWORD = "I<3python"  # შევცვალო!


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


# ── Login ─────────────────────────────────────
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin.dashboard"))
        error = "პაროლი არასწორია."
    return render_template("admin/login.html", error=error)


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


# ── Dashboard ─────────────────────────────────
@admin_bp.route("/")
@admin_required
def dashboard():
    olympiads = Olympiad.query.order_by(Olympiad.start_date.desc()).all()
    total_users = User.query.count()
    total_regs  = OlympiadRegistration.query.count()
    return render_template("admin/dashboard.html",
                           olympiads=olympiads,
                           total_users=total_users,
                           total_regs=total_regs)


# ── Olympiad registrants ──────────────────────
@admin_bp.route("/olympiad/<int:olympiad_id>")
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