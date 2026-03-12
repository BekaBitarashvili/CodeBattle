from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        data     = request.get_json(silent=True) or request.form
        email    = data.get("email", "").strip().lower()
        password = data.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.email_verified:
                err = "გთხოვთ ჯერ დაადასტუროთ ელ-ფოსტა. შეამოწმეთ inbox."
                if request.is_json:
                    return jsonify({"ok": False, "error": err}), 403
                flash(err, "warning")
                return render_template("auth/login.html")

            login_user(user, remember=bool(data.get("remember")))
            user.update_streak()
            _award_streak_badges(user)
            if request.is_json:
                return jsonify({"ok": True, "redirect": url_for("dashboard.index")})
            return redirect(url_for("dashboard.index"))

        err = "ელ-ფოსტა ან პაროლი არასწორია."
        if request.is_json:
            return jsonify({"ok": False, "error": err}), 401
        flash(err, "danger")

    return render_template("auth/login.html")


# ─────────────────────────────────────────────
#  REGISTER
#  მომხმარებელი DB-ში არ ჩაიწერება სანამ
#  მეილს არ დაადასტურებს. მონაცემები
#  token-შია დაშიფრული (itsdangerous).
# ─────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        data      = request.get_json(silent=True) or request.form
        username  = data.get("username", "").strip()
        email     = data.get("email", "").strip().lower()
        password  = data.get("password", "")
        password2 = data.get("password2", "")

        # ── Validation ────────────────────────────────
        error = None
        if not username or len(username) < 3:
            error = "სახელი უნდა იყოს მინიმუმ 3 სიმბოლო."
        elif not email or "@" not in email:
            error = "ელ-ფოსტა არასწორია."
        elif len(password) < 6:
            error = "პაროლი უნდა იყოს მინიმუმ 6 სიმბოლო."
        elif password != password2:
            error = "პაროლები არ ემთხვევა."
        elif User.query.filter_by(email=email).first():
            error = "ეს ელ-ფოსტა უკვე გამოყენებულია."
        elif User.query.filter_by(username=username).first():
            error = "ეს სახელი უკვე გამოყენებულია."

        if error:
            if request.is_json:
                return jsonify({"ok": False, "error": error}), 400
            flash(error, "danger")
            return render_template("auth/register.html")

        # ── Hash password და შევინახოთ token-ში ──────
        from werkzeug.security import generate_password_hash
        from utils.email_tokens import generate_register_token
        from utils.send_email import send_verification_email

        pw_hash = generate_password_hash(password)
        token   = generate_register_token(email, username, pw_hash)
        verify_url = url_for("auth.verify_email", token=token, _external=True)

        # ok, err_msg = send_verification_email(email, username, verify_url)
        #
        # if not ok:
        import sys
        print(f"[REG] Sending to: {email}", flush=True, file=sys.stderr)
        ok, err_msg = send_verification_email(email, username, verify_url)
        print(f"[REG] ok={ok} err={err_msg}", flush=True, file=sys.stderr)

        if not ok:
            error = "მეილის გაგზავნა ვერ მოხერხდა. სცადეთ მოგვიანებით."
            if request.is_json:
                return jsonify({"ok": False, "error": error}), 500
            flash(error, "danger")
            return render_template("auth/register.html")

        msg = "გამოგზავნილია ვერიფიკაციის ლინკი. შეამოწმეთ ელ-ფოსტა."
        if request.is_json:
            return jsonify({"ok": True, "message": msg, "needs_verify": True})
        flash(msg, "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ─────────────────────────────────────────────
#  VERIFY EMAIL
#  token-იდან ამოვიღოთ მონაცემები და
#  მხოლოდ ახლა შევქმნათ მომხმარებელი
# ─────────────────────────────────────────────
@auth_bp.route("/verify/<token>")
def verify_email(token):
    from utils.email_tokens import confirm_register_token

    result = confirm_register_token(token)
    if not result:
        flash("ვერიფიკაციის ლინკი ვადაგასულია ან არასწორია.", "danger")
        return redirect(url_for("auth.login"))

    email, username, pw_hash = result

    # თუ უკვე არსებობს (ორმაგი კლიკი)
    existing = User.query.filter_by(email=email).first()
    if existing:
        if existing.email_verified:
            flash("ელ-ფოსტა უკვე დადასტურებულია. შეგიძლიათ შეხვიდეთ.", "info")
        else:
            existing.email_verified = True
            db.session.commit()
            flash("ელ-ფოსტა დადასტურდა! 🎉 შეგიძლიათ შეხვიდეთ.", "success")
        return redirect(url_for("auth.login"))

    # ── მომხმარებლის შექმნა ──────────────────────
    # username conflict-ის შემოწმება (იშვიათი, მაგრამ შესაძლებელი)
    if User.query.filter_by(username=username).first():
        username = username + "_1"

    from werkzeug.security import generate_password_hash
    user = User(
        username       = username,
        email          = email,
        email_verified = True,
    )
    user.password_hash = pw_hash
    db.session.add(user)
    db.session.commit()

    flash("ანგარიში წარმატებით შეიქმნა! 🎉 შეგიძლიათ შეხვიდეთ.", "success")
    return redirect(url_for("auth.login"))


# ─────────────────────────────────────────────
#  RESEND VERIFICATION
# ─────────────────────────────────────────────
@auth_bp.route("/resend-verify", methods=["POST"])
def resend_verify():
    data  = request.get_json(silent=True) or request.form
    email = data.get("email", "").strip().lower()
    user  = User.query.filter_by(email=email).first()
    if user and not user.email_verified:
        _send_verify_existing(user)
    msg = "ვერიფიკაციის ლინკი გაგზავნილია. შეამოწმეთ inbox."
    if request.is_json:
        return jsonify({"ok": True, "message": msg})
    flash(msg, "success")
    return redirect(url_for("auth.login"))


# ─────────────────────────────────────────────
#  FORGOT PASSWORD
# ─────────────────────────────────────────────
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        data  = request.get_json(silent=True) or request.form
        email = data.get("email", "").strip().lower()
        user  = User.query.filter_by(email=email).first()
        if user:
            _send_reset(user)
        msg = "თუ ეს ელ-ფოსტა დარეგისტრირებულია, მიიღებთ პაროლის აღდგენის ლინკს."
        if request.is_json:
            return jsonify({"ok": True, "message": msg})
        flash(msg, "success")
        return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html")


# ─────────────────────────────────────────────
#  RESET PASSWORD
# ─────────────────────────────────────────────
@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    from utils.email_tokens import confirm_reset_token
    email = confirm_reset_token(token)
    if not email:
        flash("პაროლის აღდგენის ლინკი ვადაგასულია ან არასწორია.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first_or_404()

    if request.method == "POST":
        data      = request.get_json(silent=True) or request.form
        password  = data.get("password", "")
        password2 = data.get("password2", "")

        error = None
        if len(password) < 6:
            error = "პაროლი უნდა იყოს მინიმუმ 6 სიმბოლო."
        elif password != password2:
            error = "პაროლები არ ემთხვევა."

        if error:
            if request.is_json:
                return jsonify({"ok": False, "error": error}), 400
            flash(error, "danger")
        else:
            user.set_password(password)
            db.session.commit()
            flash("პაროლი წარმატებით შეიცვალა! 🎉 შეგიძლიათ შეხვიდეთ.", "success")
            if request.is_json:
                return jsonify({"ok": True, "redirect": url_for("auth.login")})
            return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def _send_verify_existing(user):
    """უკვე DB-ში მყოფი მომხმარებლის ვერიფიკაციის გაგზავნა."""
    from utils.email_tokens import generate_verify_token
    from utils.send_email import send_verification_email
    token      = generate_verify_token(user.email)
    verify_url = url_for("auth.verify_email", token=token, _external=True)
    try:
        send_verification_email(user.email, user.username, verify_url)
    except Exception as e:
        print(f"[MAIL ERROR] verify: {e}")


def _send_reset(user):
    from utils.email_tokens import generate_reset_token
    from utils.send_email import send_reset_email
    token     = generate_reset_token(user.email)
    reset_url = url_for("auth.reset_password", token=token, _external=True)
    try:
        send_reset_email(user.email, user.username, reset_url)
    except Exception as e:
        print(f"[MAIL ERROR] reset: {e}")


def _award_streak_badges(user):
    from models import Badge
    for slug, days in [("warrior_7", 7), ("on_fire", 30)]:
        if user.streak >= days:
            badge = Badge.query.filter_by(slug=slug).first()
            if badge and not user.has_badge(slug):
                user.badges.append(badge)
                db.session.commit()