from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import current_user, login_required
from extensions import db
from models import Task, Submission, Badge
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__)


TASKS_PER_PAGE = 20

@tasks_bp.route("/")
def index():
    difficulty = request.args.get("difficulty", "")
    page       = request.args.get("page", 1, type=int)
    search     = request.args.get("q", "").strip()

    q = Task.query.filter_by(is_active=True)
    if difficulty in ("easy", "medium", "hard"):
        q = q.filter_by(difficulty=difficulty)
    if search:
        q = q.filter(Task.title.ilike(f"%{search}%"))

    # difficulty ordering: easy < medium < hard
    diff_order = db.case(
        {"easy": 1, "medium": 2, "hard": 3},
        value=Task.difficulty
    )
    pagination = q.order_by(diff_order, Task.id.asc()).paginate(
        page=page, per_page=TASKS_PER_PAGE, error_out=False
    )
    # stats for header
    easy_count   = Task.query.filter_by(is_active=True, difficulty="easy").count()
    medium_count = Task.query.filter_by(is_active=True, difficulty="medium").count()
    hard_count   = Task.query.filter_by(is_active=True, difficulty="hard").count()
    return render_template("tasks/index.html",
                           tasks=pagination.items,
                           pagination=pagination,
                           difficulty=difficulty,
                           search=search,
                           easy_count=easy_count,
                           medium_count=medium_count,
                           hard_count=hard_count)


@tasks_bp.route("/<int:task_id>")
def detail(task_id):
    task = Task.query.get_or_404(task_id)
    user_solved = False
    if current_user.is_authenticated:
        user_solved = Submission.query.filter_by(
            user_id=current_user.id, task_id=task_id, status="accepted"
        ).first() is not None
    return render_template("tasks/detail.html", task=task, user_solved=user_solved)


@tasks_bp.route("/<int:task_id>/submit", methods=["POST"])
@login_required
def submit(task_id):
    """
    Accepts JSON: { code: str, language: str }
    Returns JSON: { ok: bool, xp_gained: int, message: str }
    Currently uses placeholder judge logic — replace with real judge later.
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}
    code     = data.get("code", "")
    language = data.get("language", "python")

    # ── Placeholder judge ─────────────────────────────
    # TODO: integrate real code execution (e.g., Judge0 API)
    status     = "accepted"
    runtime_ms = 42
    # ─────────────────────────────────────────────────

    sub = Submission(
        user_id    = current_user.id,
        task_id    = task.id,
        status     = status,
        code       = code,
        language   = language,
        runtime_ms = runtime_ms,
    )
    db.session.add(sub)
    db.session.commit()

    xp_gained = 0
    msg = ""

    if status == "accepted":
        # Only award XP if this is the first accepted submission
        already = Submission.query.filter_by(
            user_id=current_user.id, task_id=task.id, status="accepted"
        ).count()
        if already == 1:
            current_user.add_xp(task.xp)
            xp_gained = task.xp
            _check_badges(current_user, task, runtime_ms)
        msg = "სწორია! 🎉"
    else:
        msg = "შეცდომაა. სცადე ისევ."

    return jsonify({"ok": status == "accepted", "xp_gained": xp_gained, "message": msg})


@tasks_bp.route("/api/list")
def api_list():
    """JSON endpoint for dynamic filtering on frontend."""
    difficulty = request.args.get("difficulty", "easy")
    tasks = Task.query.filter_by(difficulty=difficulty, is_active=True).all()
    return jsonify([
        {"id": t.id, "title": t.title, "xp": t.xp, "difficulty": t.difficulty,
         "solves": t.solve_count()}
        for t in tasks
    ])


# ── Badge award logic ──────────────────────────────────────
def _check_badges(user, task, runtime_ms):
    def award(slug):
        badge = Badge.query.filter_by(slug=slug).first()
        if badge and not user.has_badge(slug):
            user.badges.append(badge)
            db.session.commit()

    if user.solved_count() == 1:
        award("first_blood")
    if user.solved_count() >= 50:
        award("code_samurai")
    if runtime_ms and runtime_ms < 300:
        award("speed_demon")