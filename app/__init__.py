from flask import Flask, abort, render_template

from .categories import get_categories
from . import db


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            categories=get_categories(),
            active_category=None,
        )

    @app.get("/_dev/db-check")
    def db_check():
        with db.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()

        if result != (1,):
            return {"database": "unexpected result"}, 503

        return {"database": "ok"}, 200

    @app.get("/_dev/categories")
    def categories_preview():
        return {"categories": get_categories()}

    @app.get("/categories/<slug>")
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
    
    return app
