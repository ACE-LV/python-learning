# 第十五天作业
# 主题：写一个最小 migration runner

# 作业要求：
# 1. 创建 schema_migrations 表。
# 2. 用 version 记录已经执行过的 migration。
# 3. 创建 users 表。
# 4. 给 users 表增加 email 字段。
# 5. 给 users 表增加 active 字段。
# 6. 重复运行脚本时不能重复执行已完成 migration。
# 7. 在 summary.md 写清楚 migration 的价值和风险。


import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day15_homework.db"

MIGRATIONS = [
    (
        1,
        "create users table",
        """ 
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
     """,
    ),
    (2, "add email column", "ALTER TABLE users ADD COLUMN email TEXT"),
    (
        3,
        "add active column",
        "ALTER TABLE users ADD COLUMN active INTEGER NOT NULL DEFAULT 1",
    ),
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_migration_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def has_migration(conn: sqlite3.Connection, version: int) -> bool:
    row = conn.execute(
        "SELECT version FROM schema_migrations WHERE version = ?", (version,)
    ).fetchone()
    return row is not None


def process_migrations(conn: sqlite3.Connection) -> None:
    for version, name, sql in MIGRATIONS:
        if has_migration(conn, version):
            print(f"Migration {version} already applied, skipping.")
            continue
        conn.execute(sql)
        conn.execute(
            "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
            (version, name),
        )
        print(f"Migration {version} applied:{name}")


if __name__ == "__main__":
    with get_conn() as conn:
        init_migration_table(conn)
        process_migrations(conn)
