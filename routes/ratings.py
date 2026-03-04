from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import current_user, login_required
from extensions import db
from models import User, Olympiad, OlympiadRegistration

ratings_bp = Blueprint("ratings", __name__)


@ratings_bp.route("/")
def index():
    top_users = User.query.order_by(User.xp.desc()).limit(50).all()
    return render_template("ratings/index.html", users=top_users)


@ratings_bp.route("/api")
def api():
    top = User.query.order_by(User.xp.desc()).limit(20).all()
    return jsonify([
        {"rank": i+1, "username": u.username, "xp": u.xp,
         "level": u.level, "streak": u.streak,
         "badges": [{"emoji": b.emoji, "name": b.name_ka} for b in u.badges.all()]}
        for i, u in enumerate(top)
    ])
