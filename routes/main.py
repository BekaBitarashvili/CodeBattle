from flask import Blueprint, render_template, session, request, redirect, url_for, abort

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


@main_bp.route("/news/<int:news_id>")
def news_detail(news_id):
    from models import News
    item = News.query.filter_by(id=news_id, is_published=True).first_or_404()
    # prev / next for navigation
    prev_item = (
        News.query.filter_by(is_published=True)
        .filter(News.created_at < item.created_at)
        .order_by(News.created_at.desc())
        .first()
    )
    next_item = (
        News.query.filter_by(is_published=True)
        .filter(News.created_at > item.created_at)
        .order_by(News.created_at.asc())
        .first()
    )
    return render_template("news_detail.html", item=item, prev_item=prev_item, next_item=next_item)


@main_bp.route("/set-language/<lang>")
def set_language(lang):
    if lang in ("ka", "en"):
        session["lang"] = lang
    return redirect(request.referrer or url_for("main.index"))