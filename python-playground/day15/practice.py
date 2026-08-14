# 第十五天练习题
# 主题：数据库迁移

# 练习 1：新增第 3 个 migration。
# 要求：给 users 表增加 active INTEGER NOT NULL DEFAULT 1。

from sqlite3 import connect
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
        "add active column",
        "ALTER TABLE users ADD COLUMN active INTEGER NOT NULL DEFAULT 1",
    ),
]


def get_conn() -> connect:
    conn = connect("practice.db")
    conn.row_factory = connect.Row
    return conn


def init_migration_table(conn: connect) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)


def has_migration(conn: connect, version: int) -> bool:
    row = conn.execute(
        "SELECT version FROM schema_migrations WHERE version = ?",
        (version,),
    ).fetchone()
    return row is not None


def apply_migration(conn: connect, version: int, name: str, sql: str) -> None:
    if has_migration(conn, version):
        print(f"Migration {version} already applied, skipping.")
        return
    conn.execute(sql)
    conn.execute(
        "INSERT INTO schema_migrations (version,name) VALUES (?,?)",
        (version, name),
    )
    print(f"Migration {version} applied successfully.")


if __name__ == "__main__":
    with get_conn() as conn:
        init_migration_table(conn)
        for version, name, sql in MIGRATIONS:
            apply_migration(conn, version, name, sql)


# 练习 2：修改 print_state，输出 active 字段。

# 练习 3：重复运行 migration_demo.py。
# 要求：第 1、2、3 个 migration 都只执行一次。

# 练习 4：新增 courses 表 migration。
# 字段：id、title、level。

# 练习 5：思考：为什么生产数据库不能随便 DROP TABLE？
