
from hashlib import sha256
from pathlib import Path

from app.db import get_connection

MIGRATIONS_DIR = (
    Path(__file__).resolve().parent.parent / "migrations"
)

MIGRATION_LOCK_ID = 712026

def main():
    applied = []
    skipped = []

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pg_advisory_xact_lock(%s)",
                (MIGRATION_LOCK_ID,),
            )

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

                    skipped.append(path.name)
                    continue

                cursor.execute(content)

                cursor.execute(
                    "INSERT INTO schema_migrations "
                    "(filename, checksum) VALUES (%s, %s)",
                    (path.name, checksum),
                )

                applied.append(path.name)


    for filename in skipped:
        print(f"SKIP: {filename}")

    for filename in applied:
        print(f"APPLIED: {filename}")


if __name__ == "__main__":
    main()
