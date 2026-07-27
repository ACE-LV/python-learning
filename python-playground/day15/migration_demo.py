import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day15_migration.db"

MIGRATIONS = [
    (
        1,
        "create users table",
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """,
    ),
    (
        2,
        "add email column",
        "ALTER TABLE users ADD COLUMN email TEXT",
    ),
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_migration_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def has_migration(conn: sqlite3.Connection, version: int) -> bool:
    row = conn.execute(
        "SELECT version FROM schema_migrations WHERE version = ?",
        (version,),
    ).fetchone()
    return row is not None


def apply_migrations() -> None:
    with get_conn() as conn:
        init_migration_table(conn)

        for version, name, sql in MIGRATIONS:
            if has_migration(conn, version):
                print(f"skip migration {version}: {name}")
                continue

            print(f"apply migration {version}: {name}")
            conn.execute(sql)
            conn.execute(
                "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
                (version, name),
            )


def seed_user() -> None:
    with get_conn() as conn:
        existing = conn.execute("SELECT id FROM users WHERE name = ?", ("Alice",)).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO users (name, role, email) VALUES (?, ?, ?)",
                ("Alice", "frontend", "alice@example.com"),
            )


def print_state() -> None:
    with get_conn() as conn:
        columns = conn.execute("PRAGMA table_info(users)").fetchall()
        users = conn.execute("SELECT id, name, role, email FROM users").fetchall()
        migrations = conn.execute("SELECT version, name, applied_at FROM schema_migrations").fetchall()

    print("\nusers columns:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

    print("\nusers rows:")
    for user in users:
        print(dict(user))

    print("\napplied migrations:")
    for migration in migrations:
        print(dict(migration))


if __name__ == "__main__":
    apply_migrations()
    seed_user()
    print_state()
