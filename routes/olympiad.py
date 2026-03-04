from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from extensions import db
from models import Olympiad, OlympiadRegistration
from datetime import datetime

olympiad_bp = Blueprint("olympiad", __name__)


@olympiad_bp.route("/")
def index():
    olympiads = Olympiad.query.filter_by(is_active=True).order_by(Olympiad.start_date.desc()).all()
    return render_template("olympiad/index.html", olympiads=olympiads)


@olympiad_bp.route("/<int:olympiad_id>")
def detail(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    registered = False
    if current_user.is_authenticated:
        registered = OlympiadRegistration.query.filter_by(
            user_id=current_user.id, olympiad_id=olympiad_id
        ).first() is not None
    return render_template("olympiad/detail.html", olympiad=olympiad, registered=registered)


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
