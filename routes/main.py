from flask import Blueprint, render_template, session, request, redirect, url_for

main_bp = Blueprint("main", __name__)

NEWS_PER_PAGE = 10


@main_bp.route("/")
def index():
    from models import News
    page = request.args.get("page", 1, type=int)
    pagination = (
        News.query
        .filter_by(is_published=True)
        .order_by(News.created_at.desc())
        .paginate(page=page, per_page=NEWS_PER_PAGE, error_out=False)
    )
    return render_template("index.html", pagination=pagination, news=pagination.items)


@main_bp.route("/set-language/<lang>")
def set_language(lang):
    if lang in ("ka", "en"):
        session["lang"] = lang
    return redirect(request.referrer or url_for("main.index"))
