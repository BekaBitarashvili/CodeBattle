from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        email    = data.get("email", "").strip().lower()
        password = data.get("password", "")
        remember = bool(data.get("remember", False))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.update_streak()
            _award_streak_badges(user)
            if request.is_json:
                return jsonify({"ok": True, "redirect": url_for("dashboard.index")})
            return redirect(url_for("dashboard.index"))

        if request.is_json:
            return jsonify({"ok": False, "error": "ელ-ფოსტა ან პაროლი არასწორია."}), 401
        flash("ელ-ფოსტა ან პაროლი არასწორია.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        username = data.get("username", "").strip()
        email    = data.get("email", "").strip().lower()
        password = data.get("password", "")

        error = None
        if not username or len(username) < 3:
            error = "სახელი უნდა იყოს მინიმუმ 3 სიმბოლო."
        elif not email or "@" not in email:
            error = "ელ-ფოსტა არასწორია."
        elif len(password) < 6:
            error = "პაროლი უნდა იყოს მინიმუმ 6 სიმბოლო."
        elif User.query.filter_by(email=email).first():
            error = "ეს ელ-ფოსტა უკვე გამოყენებულია."
        elif User.query.filter_by(username=username).first():
            error = "ეს სახელი უკვე გამოყენებულია."

        if error:
            if request.is_json:
                return jsonify({"ok": False, "error": error}), 400
            flash(error, "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            # Grant First Blood badge if first solve
            login_user(user)
            user.update_streak()
            if request.is_json:
                return jsonify({"ok": True, "redirect": url_for("dashboard.index")})
            return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# ── Internal helpers ──────────────────────────────────────
def _award_streak_badges(user: User):
    from models import Badge
    if user.streak >= 7:
        badge = Badge.query.filter_by(slug="warrior_7").first()
        if badge and not user.has_badge("warrior_7"):
            user.badges.append(badge)
            db.session.commit()
    if user.streak >= 30:
        badge = Badge.query.filter_by(slug="on_fire").first()
        if badge and not user.has_badge("on_fire"):
            user.badges.append(badge)
            db.session.commit()
