
from hashlib import sha256
from pathlib import Path

from app.db import get_connection


MIGRATIONS_DIR = (
    Path(__file__).resolve().parent.parent / "migrations"
)


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    filename TEXT PRIMARY KEY,
                    checksum TEXT NOT NULL,
                    applied_at TIMESTAMPTZ
                        NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

            for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
                content = path.read_text(encoding="utf-8")
                checksum = sha256(content.encode("utf-8")).hexdigest()

                cursor.execute(
                    "SELECT checksum FROM schema_migrations "
                    "WHERE filename = %s",
                    (path.name,),
                )

                row = cursor.fetchone()

                if row is not None:
                    if row[0] != checksum:
                        raise RuntimeError(
                            f"Applied migration was modified: {path.name}"
                        )

                    print(f"SKIP: {path.name}")
                    continue

                cursor.execute(content)

                cursor.execute(
                    "INSERT INTO schema_migrations "
                    "(filename, checksum) VALUES (%s, %s)",
                    (path.name, checksum),
                )

                print(f"APPLIED: {path.name}")


if __name__ == "__main__":
    main()
