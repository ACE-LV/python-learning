# 第十五天练习题
# 主题：数据库迁移

# 练习 1：新增第 3 个 migration。
# 要求：给 users 表增加 active INTEGER NOT NULL DEFAULT 1。

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "practice.db"

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
    (
        3,
        "add active column",
        "ALTER TABLE users ADD COLUMN active INTEGER NOT NULL DEFAULT 1",
    ),
    (
        4,
        "add courses table",
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            level TEXT NOT NULL
        )
        """,
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
        "SELECT version FROM schema_migrations WHERE version = ?",
        (version,),
    ).fetchone()
    return row is not None


def apply_migration(
    conn: sqlite3.Connection, version: int, name: str, sql: str
) -> None:
    if has_migration(conn, version):
        print(f"Migration {version} already applied, skipping.")
        return
    conn.execute(sql)
    conn.execute(
        "INSERT INTO schema_migrations (version,name) VALUES (?,?)",
        (version, name),
    )
    print(f"Migration {version} applied successfully.")


def print_state() -> None:
    with get_conn() as conn:
        columns = conn.execute("PRAGMA table_info(users)").fetchall()
        migrations = conn.execute(
            "SELECT version, name, applied_at FROM schema_migrations ORDER BY version"
        ).fetchall()

    print("\nusers columns:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

    print("\napplied migrations:")
    for migration in migrations:
        print(dict(migration))


if __name__ == "__main__":
    with get_conn() as conn:
        init_migration_table(conn)
        for version, name, sql in MIGRATIONS:
            apply_migration(conn, version, name, sql)
    print_state()


# 练习 2：修改 print_state，输出 active 字段。（已完成）


# 练习 3：重复运行 migration_demo.py。
# 要求：第 1、2、3 个 migration 都只执行一次。

# 练习 4：新增 courses 表 migration。
# 字段：id、title、level。

# 练习 5：生产数据库不能随便 DROP TABLE，因为会直接删除表结构和全部数据，
# 还可能破坏外键关系、导致服务报错；执行前需要备份、评审和可回滚方案。
