from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import Submission

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    # ── Recent Activity: მხოლოდ unique ამოცანები, ბოლო 8 ──
    # თითოეული ამოცანიდან ბოლო accepted submission
    seen_task_ids = set()
    unique_recent = []

    all_accepted = (
        Submission.query
        .filter_by(user_id=current_user.id, status="accepted")
        .order_by(Submission.submitted_at.desc())
        .limit(50)
        .all()
    )

    for sub in all_accepted:
        if sub.task_id not in seen_task_ids:
            seen_task_ids.add(sub.task_id)
            unique_recent.append(sub)
        if len(unique_recent) >= 8:
            break

    my_badges = current_user.badges.all()

    return render_template(
        "dashboard/dashboard_index.html",
        user=current_user,
        recent=unique_recent,
        badges=my_badges,
    )


@dashboard_bp.route("/api/stats")
@login_required
def stats():
    return jsonify({
        "xp":          current_user.xp,
        "level":       current_user.level,
        "streak":      current_user.streak,
        "solved":      current_user.solved_count(),
        "xp_progress": current_user.xp_progress_pct(),
        "xp_to_next":  current_user.xp_to_next_level(),
    })