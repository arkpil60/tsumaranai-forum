from app.db import get_connection


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_user, current_database();"
            )
            print(cursor.fetchone())


if __name__ == "__main__":
    main()
