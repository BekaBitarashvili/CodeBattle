import os
import json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import current_user, login_required
from extensions import db
from models import Olympiad, OlympiadRegistration, User, Task, Submission
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
    total_tasks = Task.query.count()
    return render_template("admin/dashboard.html",
                           olympiads=olympiads,
                           total_users=total_users,
                           total_regs=total_regs,
                           total_tasks=total_tasks)


# ── Olympiad Create ───────────────────────────
@admin_bp.route("/olympiad/new", methods=["GET", "POST"])
@login_required
@admin_required
def olympiad_new():
    if request.method == "POST":
        try:
            o = Olympiad(
                title_ka   = request.form["title_ka"],
                title_en   = request.form["title_en"],
                start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%dT%H:%M"),
                end_date   = datetime.strptime(request.form["end_date"],   "%Y-%m-%dT%H:%M"),
                prize_info = request.form.get("prize_info", ""),
                is_active  = "is_active" in request.form,
            )
            db.session.add(o)
            db.session.commit()
            flash("ოლიმპიადა შეიქმნა! ✅", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            flash(f"შეცდომა: {e}", "danger")
    return render_template("admin/olympiad_form.html", olympiad=None, action="new")


# ── Olympiad Edit ─────────────────────────────
@admin_bp.route("/olympiad/<int:olympiad_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def olympiad_edit(olympiad_id):
    o = Olympiad.query.get_or_404(olympiad_id)
    if request.method == "POST":
        try:
            o.title_ka   = request.form["title_ka"]
            o.title_en   = request.form["title_en"]
            o.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%dT%H:%M")
            o.end_date   = datetime.strptime(request.form["end_date"],   "%Y-%m-%dT%H:%M")
            o.prize_info = request.form.get("prize_info", "")
            o.is_active  = "is_active" in request.form
            db.session.commit()
            flash("ოლიმპიადა განახლდა! ✅", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            flash(f"შეცდომა: {e}", "danger")
    return render_template("admin/olympiad_form.html", olympiad=o, action="edit")


# ── Olympiad Delete ───────────────────────────
@admin_bp.route("/olympiad/<int:olympiad_id>/delete", methods=["POST"])
@login_required
@admin_required
def olympiad_delete(olympiad_id):
    o = Olympiad.query.get_or_404(olympiad_id)
    OlympiadRegistration.query.filter_by(olympiad_id=olympiad_id).delete()
    db.session.delete(o)
    db.session.commit()
    flash("ოლიმპიადა წაიშალა.", "success")
    return redirect(url_for("admin.dashboard"))


# ── Olympiad Registrants ──────────────────────
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


# ── Users List ────────────────────────────────
@admin_bp.route("/users")
@login_required
@admin_required
def users():
    search = request.args.get("q", "").strip()
    query  = User.query
    if search:
        query = query.filter(
            User.username.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%")
        )
    all_users = query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users, search=search)


# ── User Edit ─────────────────────────────────
@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def user_edit(user_id):
    u = User.query.get_or_404(user_id)
    if request.method == "POST":
        try:
            u.username       = request.form["username"]
            u.email          = request.form["email"]
            u.xp             = int(request.form.get("xp", u.xp))
            u.level          = int(request.form.get("level", u.level))
            u.streak         = int(request.form.get("streak", u.streak))
            u.email_verified = "email_verified" in request.form
            new_pass = request.form.get("new_password", "").strip()
            if new_pass:
                u.set_password(new_pass)
            db.session.commit()
            flash(f"{u.username} — განახლდა! ✅", "success")
            return redirect(url_for("admin.users"))
        except Exception as e:
            flash(f"შეცდომა: {e}", "danger")
    return render_template("admin/user_form.html", user=u)


# ── User Delete ───────────────────────────────
@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def user_delete(user_id):
    u = User.query.get_or_404(user_id)
    if u.email.lower() in [e.strip().lower() for e in os.environ.get("ADMIN_EMAILS", "").split(",")]:
        flash("ადმინის წაშლა შეუძლებელია.", "danger")
        return redirect(url_for("admin.users"))
    Submission.query.filter_by(user_id=user_id).delete()
    OlympiadRegistration.query.filter_by(user_id=user_id).delete()
    db.session.delete(u)
    db.session.commit()
    flash("მომხმარებელი წაიშალა.", "success")
    return redirect(url_for("admin.users"))


# ── Tasks List ────────────────────────────────
@admin_bp.route("/tasks")
@login_required
@admin_required
def tasks():
    search     = request.args.get("q", "").strip()
    difficulty = request.args.get("difficulty", "")
    query      = Task.query
    if search:
        query = query.filter(
            Task.title_ka.ilike(f"%{search}%") |
            Task.title_en.ilike(f"%{search}%")
        )
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    all_tasks = query.order_by(Task.id.asc()).all()
    return render_template("admin/tasks.html", tasks=all_tasks, search=search, difficulty=difficulty)


# ── Task New ──────────────────────────────────
@admin_bp.route("/tasks/new", methods=["GET", "POST"])
@login_required
@admin_required
def task_new():
    if request.method == "POST":
        try:
            # test cases JSON ვალიდაცია
            tc_raw = request.form.get("test_cases", "[]").strip()
            json.loads(tc_raw)  # validate

            t = Task(
                title_ka       = request.form["title_ka"],
                title_en       = request.form["title_en"],
                difficulty     = request.form["difficulty"],
                xp             = int(request.form.get("xp", 30)),
                description_ka = request.form.get("description_ka", ""),
                description_en = request.form.get("description_en", ""),
                category_ka    = request.form.get("category_ka", ""),
                category_en    = request.form.get("category_en", ""),
                time_limit     = float(request.form.get("time_limit", 2.0)),
                memory_limit   = int(request.form.get("memory_limit", 256)),
                test_cases     = tc_raw,
                is_active      = "is_active" in request.form,
            )
            db.session.add(t)
            db.session.commit()
            flash(f"ტასკი '{t.title_ka}' შეიქმნა! ✅", "success")
            return redirect(url_for("admin.tasks"))
        except json.JSONDecodeError:
            flash("Test Cases — JSON ფორმატი არასწორია.", "danger")
        except Exception as e:
            flash(f"შეცდომა: {e}", "danger")
    return render_template("admin/task_form.html", task=None, action="new")


# ── Task Edit ─────────────────────────────────
@admin_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def task_edit(task_id):
    t = Task.query.get_or_404(task_id)
    if request.method == "POST":
        try:
            tc_raw = request.form.get("test_cases", "[]").strip()
            json.loads(tc_raw)

            t.title_ka       = request.form["title_ka"]
            t.title_en       = request.form["title_en"]
            t.difficulty     = request.form["difficulty"]
            t.xp             = int(request.form.get("xp", t.xp))
            t.description_ka = request.form.get("description_ka", "")
            t.description_en = request.form.get("description_en", "")
            t.category_ka    = request.form.get("category_ka", "")
            t.category_en    = request.form.get("category_en", "")
            t.time_limit     = float(request.form.get("time_limit", 2.0))
            t.memory_limit   = int(request.form.get("memory_limit", 256))
            t.test_cases     = tc_raw
            t.is_active      = "is_active" in request.form
            db.session.commit()
            flash(f"ტასკი '{t.title_ka}' განახლდა! ✅", "success")
            return redirect(url_for("admin.tasks"))
        except json.JSONDecodeError:
            flash("Test Cases — JSON ფორმატი არასწორია.", "danger")
        except Exception as e:
            flash(f"შეცდომა: {e}", "danger")
    return render_template("admin/task_form.html", task=t, action="edit")


# ── Task Delete ───────────────────────────────
@admin_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
@admin_required
def task_delete(task_id):
    t = Task.query.get_or_404(task_id)
    Submission.query.filter_by(task_id=task_id).delete()
    db.session.delete(t)
    db.session.commit()
    flash("ტასკი წაიშალა.", "success")
    return redirect(url_for("admin.tasks"))