from flask import Blueprint, abort, render_template

from .categories import get_categories


forum_bp = Blueprint("forum", __name__)


@forum_bp.get("/")
def index():
    return render_template(
        "index.html",
        categories=get_categories(),
        active_category=None,
    )


@forum_bp.get("/categories/<slug>")
def category_page(slug):
    categories = get_categories()

    category = next(
        (item for item in categories if item["slug"] == slug),
        None,
    )

    if category is None:
        abort(404)

    return render_template(
        "index.html",
        categories=categories,
        active_category=category,
    )
