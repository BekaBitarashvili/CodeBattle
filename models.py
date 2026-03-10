from datetime import datetime, date
from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# ─────────────────────────────────────────────────────────
#  News / Announcement
# ─────────────────────────────────────────────────────────
class News(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title_ka     = db.Column(db.String(200), nullable=False)
    title_en     = db.Column(db.String(200), nullable=False)
    body_ka      = db.Column(db.Text,        nullable=False)
    body_en      = db.Column(db.Text,        nullable=False)
    category_ka  = db.Column(db.String(64),  default="სიახლე")
    category_en  = db.Column(db.String(64),  default="News")
    emoji        = db.Column(db.String(8),   default="📢")
    image_url    = db.Column(db.String(512),  nullable=True)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow)
    is_published = db.Column(db.Boolean,     default=True)

    def __repr__(self):
        return f"<News {self.id}: {self.title_en}>"


# ─────────────────────────────────────────────────────────
#  User ↔ Badge  (M2M)
# ─────────────────────────────────────────────────────────
user_badges = db.Table(
    "user_badges",
    db.Column("user_id",  db.Integer, db.ForeignKey("user.id"),  primary_key=True),
    db.Column("badge_id", db.Integer, db.ForeignKey("badge.id"), primary_key=True),
    db.Column("earned_at", db.DateTime, default=datetime.utcnow),
)


# ─────────────────────────────────────────────────────────
#  User
# ─────────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    # XP & level
    xp            = db.Column(db.Integer, default=0)
    level         = db.Column(db.Integer, default=1)

    # Streak
    streak        = db.Column(db.Integer, default=0)
    longest_streak= db.Column(db.Integer, default=0)
    last_login_date = db.Column(db.Date,  nullable=True)

    # Email verification
    email_verified = db.Column(db.Boolean, default=False)

    # Language preference  ("ka" | "en")
    language      = db.Column(db.String(4), default="ka")

    # Relationships
    submissions   = db.relationship("Submission", backref="user", lazy="dynamic")
    badges        = db.relationship("Badge", secondary=user_badges, backref="users", lazy="dynamic")
    olympiad_registrations = db.relationship("OlympiadRegistration", backref="user", lazy="dynamic")

    # ── Password helpers ──────────────────────────────
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ── XP helpers ────────────────────────────────────
    def add_xp(self, amount: int):
        self.xp += amount
        self.level = 1 + self.xp // 500
        db.session.commit()

    # ── Streak helpers ────────────────────────────────
    def update_streak(self):
        today = date.today()
        if self.last_login_date == today:
            return
        if self.last_login_date and (today - self.last_login_date).days == 1:
            self.streak += 1
        else:
            self.streak = 1
        self.last_login_date = today
        if self.streak > self.longest_streak:
            self.longest_streak = self.streak
        db.session.commit()

    def xp_to_next_level(self) -> int:
        return 500 - (self.xp % 500)

    def xp_progress_pct(self) -> int:
        return int((self.xp % 500) / 500 * 100)

    def has_badge(self, slug: str) -> bool:
        return self.badges.filter_by(slug=slug).first() is not None

    def solved_count(self) -> int:
        return self.submissions.filter_by(status="accepted").count()

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────────────────
#  Task
# ─────────────────────────────────────────────────────────
class Task(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(128), nullable=False)
    difficulty   = db.Column(db.String(16),  nullable=False)
    xp           = db.Column(db.Integer,     default=30)
    # Full problem statement (Markdown supported)
    description  = db.Column(db.Text,        nullable=True)
    # JSON array: [{"input": "...", "output": "...", "explanation": "..."}]
    # First 2 are shown to user, rest are hidden judge tests
    test_cases   = db.Column(db.Text,        nullable=True)
    # Limits
    time_limit   = db.Column(db.Float,       default=2.0)    # seconds
    memory_limit = db.Column(db.Integer,     default=256)    # MB
    # Category tag e.g. "Math", "DP", "Greedy", "Strings"
    category     = db.Column(db.String(64),  nullable=True)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow)
    is_active    = db.Column(db.Boolean,     default=True)

    submissions  = db.relationship("Submission", backref="task", lazy="dynamic")

    def solve_count(self):
        return self.submissions.filter_by(status="accepted").count()

    def get_test_cases(self):
        import json
        try:
            return json.loads(self.test_cases or "[]")
        except Exception:
            return []

    def get_visible_tests(self):
        """First 2 test cases shown to user as examples."""
        return self.get_test_cases()[:2]

    def __repr__(self):
        return f"<Task {self.title} [{self.difficulty}]>"


# ─────────────────────────────────────────────────────────
#  Submission
# ─────────────────────────────────────────────────────────
class Submission(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    task_id     = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    status      = db.Column(db.String(16), default="pending")
    code        = db.Column(db.Text,       nullable=True)
    language    = db.Column(db.String(32), default="python")
    runtime_ms  = db.Column(db.Integer,    nullable=True)
    submitted_at= db.Column(db.DateTime,   default=datetime.utcnow)

    def __repr__(self):
        return f"<Submission user={self.user_id} task={self.task_id} {self.status}>"


# ─────────────────────────────────────────────────────────
#  Badge
# ─────────────────────────────────────────────────────────
class Badge(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    slug           = db.Column(db.String(64),  unique=True, nullable=False)
    name_ka        = db.Column(db.String(128),  nullable=False)
    name_en        = db.Column(db.String(128),  nullable=False)
    emoji          = db.Column(db.String(8),    nullable=False)
    description_ka = db.Column(db.String(256),  nullable=True)
    description_en = db.Column(db.String(256),  nullable=True)

    def __repr__(self):
        return f"<Badge {self.slug}>"


# ─────────────────────────────────────────────────────────
#  Olympiad
# ─────────────────────────────────────────────────────────
class Olympiad(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title_ka    = db.Column(db.String(128), nullable=False)
    title_en    = db.Column(db.String(128), nullable=False)
    start_date  = db.Column(db.DateTime,    nullable=False)
    end_date    = db.Column(db.DateTime,    nullable=False)
    prize_info  = db.Column(db.Text,        nullable=True)
    is_active   = db.Column(db.Boolean,     default=True)

    registrations = db.relationship("OlympiadRegistration", backref="olympiad", lazy="dynamic")

    @property
    def is_ongoing(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date

    @property
    def participant_count(self):
        return self.registrations.count()

    def __repr__(self):
        return f"<Olympiad {self.title_en}>"


class OlympiadRegistration(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"),     nullable=False)
    olympiad_id = db.Column(db.Integer, db.ForeignKey("olympiad.id"), nullable=False)
    score       = db.Column(db.Integer, default=0)
    rank        = db.Column(db.Integer, nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)