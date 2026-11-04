from psycopg.rows import dict_row

from .db import get_connection


def get_categories():
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    slug,
                    title,
                    description
                FROM categories
                ORDER BY display_order, id;
            """)

            return cursor.fetchall()


def create_category(slug, title, description=""):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO categories (slug, title, description)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (slug, title, description),
            )

            return cursor.fetchone()[0]
