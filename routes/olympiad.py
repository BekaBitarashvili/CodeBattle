from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_required
from extensions import db
from models import Olympiad, OlympiadRegistration
from datetime import datetime

olympiad_bp = Blueprint("olympiad", __name__)

OLYMPIADS_PER_PAGE = 5


@olympiad_bp.route("/")
def index():
    _seed_olympiads()
    page = request.args.get("page", 1, type=int)
    pagination = (
        Olympiad.query
        .filter_by(is_active=True)
        .order_by(Olympiad.start_date.desc())
        .paginate(page=page, per_page=OLYMPIADS_PER_PAGE, error_out=False)
    )
    return render_template("olympiad/index.html",
                           pagination=pagination,
                           olympiads=pagination.items,
                           now=datetime.utcnow())


@olympiad_bp.route("/<int:olympiad_id>")
def detail(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    registered = False
    if current_user.is_authenticated:
        registered = OlympiadRegistration.query.filter_by(
            user_id=current_user.id, olympiad_id=olympiad_id
        ).first() is not None
    return render_template("olympiad/detail.html", olympiad=olympiad, registered=registered, now_dt=datetime.utcnow())


@olympiad_bp.route("/<int:olympiad_id>/register", methods=["POST"])
@login_required
def register(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    existing = OlympiadRegistration.query.filter_by(
        user_id=current_user.id, olympiad_id=olympiad_id
    ).first()
    if existing:
        return jsonify({"ok": False, "error": "უკვე დარეგისტრირებული ხარ."})
    reg = OlympiadRegistration(user_id=current_user.id, olympiad_id=olympiad_id)
    db.session.add(reg)
    db.session.commit()
    return jsonify({"ok": True, "message": "წარმატებით დარეგისტრირდი! 🏆"})


def _seed_olympiads():
    """Add demo olympiads if none exist."""
    if Olympiad.query.first():
        return
    from datetime import timedelta
    now = datetime.utcnow()
    olympiads = [
        Olympiad(
            title_ka="მარტის კოდინგის ოლიმპიადა 2026",
            title_en="March Coding Olympiad 2026",
            start_date=now + timedelta(days=13),
            end_date=now + timedelta(days=20),
            prize_info="MacBook Pro M3 · iPad Pro · AirPods Pro",
            is_active=True,
        ),
        Olympiad(
            title_ka="Python Challenge — გაზაფხული 2026",
            title_en="Python Challenge — Spring 2026",
            start_date=now - timedelta(days=5),
            end_date=now + timedelta(days=2),
            prize_info="iPad Mini · Apple Watch · Gift Cards",
            is_active=True,
        ),
    ]
    db.session.add_all(olympiads)
    db.session.commit()