from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import Submission, Task

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    recent_submissions = (
        Submission.query
        .filter_by(user_id=current_user.id, status="accepted")
        .order_by(Submission.submitted_at.desc())
        .limit(10)
        .all()
    )
    my_badges = current_user.badges.all()
    return render_template(
        "dashboard/index.html",
        user=current_user,
        recent=recent_submissions,
        badges=my_badges,
    )


@dashboard_bp.route("/api/stats")
@login_required
def stats():
    return jsonify({
        "xp":           current_user.xp,
        "level":        current_user.level,
        "streak":       current_user.streak,
        "solved":       current_user.solved_count(),
        "xp_progress":  current_user.xp_progress_pct(),
        "xp_to_next":   current_user.xp_to_next_level(),
    })
