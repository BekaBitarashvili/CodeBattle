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
        from sqlalchemy import or_
        q = q.filter(or_(
            Task.title_ka.ilike(f"%{search}%"),
            Task.title_en.ilike(f"%{search}%")
        ))

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
    return render_template("tasks/tasks_index.html",
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
    Returns JSON: { ok, status, xp_gained, message, passed, total,
                    runtime_ms, error_message, first_fail }
    """
    task = Task.query.get_or_404(task_id)
    data     = request.get_json(silent=True) or {}
    code     = data.get("code", "").strip()
    language = data.get("language", "python").lower()

    if not code:
        return jsonify({"ok": False, "status": "error",
                        "message": "კოდი ცარიელია.", "xp_gained": 0}), 400

    # ── Judge0 evaluation ────────────────────────────
    from utils.judge import judge_task
    result = judge_task(code, language, task)
    # ─────────────────────────────────────────────────

    status     = result["status"]
    runtime_ms = result["runtime_ms"]

    # Save submission
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
    if status == "accepted":
        first_accepted = Submission.query.filter_by(
            user_id=current_user.id, task_id=task.id, status="accepted"
        ).count()
        if first_accepted == 1:   # just saved above = first time
            current_user.add_xp(task.xp)
            xp_gained = task.xp
            _check_badges(current_user, task, runtime_ms)

    # Human-readable message (Georgian)
    MSG = {
        "accepted":            "სწორია! ყველა ტესტი გავიდა ✅",
        "wrong_answer":        "არასწორი პასუხი ❌",
        "compilation_error":   "კომპილაციის შეცდომა 🔧",
        "time_limit_exceeded": "დრო ამოიწურა ⏱",
        "runtime_error":       "Runtime შეცდომა 💥",
        "memory_limit_exceeded": "მეხსიერება ამოიწურა 📦",
        "internal_error":      "სერვერის შეცდომა, სცადე ხელახლა",
        "error":               "Judge0 შეცდომა — შეამოწმე კონფიგი",
    }

    return jsonify({
        "ok":            result["ok"],
        "status":        status,
        "xp_gained":     xp_gained,
        "message":       MSG.get(status, status),
        "passed":        result["passed"],
        "total":         result["total"],
        "runtime_ms":    runtime_ms,
        "error_message": result.get("error_message", ""),
        "first_fail":    result.get("first_fail"),
    })


@tasks_bp.route("/api/list")
def api_list():
    """JSON endpoint for dynamic filtering on frontend."""
    difficulty = request.args.get("difficulty", "easy")
    tasks = Task.query.filter_by(difficulty=difficulty, is_active=True).all()
    from flask import session as flask_session
    lang = flask_session.get("lang", "ka")
    return jsonify([
        {"id": t.id,
         "title": t.get_title(lang),
         "xp": t.xp,
         "difficulty": t.difficulty,
         "category": t.get_category(lang),
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