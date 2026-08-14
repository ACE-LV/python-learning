import sqlite3
from pathlib import Path

# 第 15 天主题：数据库迁移 migration。
# migration 的目标：用代码记录“数据库结构怎么一步步变化”，而不是手动改库。

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day15_migration.db"

# MIGRATIONS 是迁移清单。
# 每一项包含：版本号、名称、要执行的 SQL。
# version 很重要：它让脚本知道哪些迁移已经执行过，避免重复 ALTER TABLE。
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
        # ALTER TABLE 是表结构变更。
        # 注意：如果重复执行 ADD COLUMN email，会报 duplicate column name。
        # 所以必须配合 schema_migrations 版本表，保证只执行一次。
        "ALTER TABLE users ADD COLUMN email TEXT",
    ),
]


def get_conn() -> sqlite3.Connection:
    # 创建 SQLite 连接。
    # row_factory=sqlite3.Row 可以让查询结果像 dict 一样通过列名读取。
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_migration_table(conn: sqlite3.Connection) -> None:
    # schema_migrations 是迁移版本表。
    # 它不是业务表，而是用来记录“哪些 migration 已经执行过”。
    # 真实项目里的 Alembic/Flyway/Liquibase 也都有类似版本表。
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)


def has_migration(conn: sqlite3.Connection, version: int) -> bool:
    # 判断某个版本号是否已经执行过。
    # 如果 schema_migrations 里有 version=2，说明第 2 个 migration 已完成，不能再执行。
    row = conn.execute(
        "SELECT version FROM schema_migrations WHERE version = ?",
        (version,),
    ).fetchone()
    return row is not None


def apply_migrations() -> None:
    # 迁移执行器。
    # 核心流程：先确保版本表存在 -> 遍历迁移清单 -> 跳过已执行版本 -> 执行新版本 -> 记录版本。
    with get_conn() as conn:
        init_migration_table(conn)

        for version, name, sql in MIGRATIONS:
            if has_migration(conn, version):
                # 已执行过就跳过，因此脚本可以反复运行。
                print(f"skip migration {version}: {name}")
                continue

            print(f"apply migration {version}: {name}")
            # 执行真正的表结构变更 SQL。
            conn.execute(sql)
            # 结构变更成功后，再写入 schema_migrations。
            # 如果 SQL 失败，这里不会执行，下一次还可以重试。
            conn.execute(
                "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
                (version, name),
            )


def seed_user() -> None:
    # 写入一条演示数据。
    # 这不是 migration，只是为了运行脚本后能看到 users 表里有数据。
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE name = ?", ("Alice",)
        ).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO users (name, role, email) VALUES (?, ?, ?)",
                ("Alice", "frontend", "alice@example.com"),
            )


def print_state() -> None:
    # 打印当前数据库状态，帮助你观察 migration 的结果。
    with get_conn() as conn:
        # PRAGMA table_info(users) 是 SQLite 查看表字段结构的命令。
        columns = conn.execute("PRAGMA table_info(users)").fetchall()
        users = conn.execute("SELECT id, name, role, email FROM users").fetchall()
        # 查看已经执行过哪些 migration。
        migrations = conn.execute(
            "SELECT version, name, applied_at FROM schema_migrations"
        ).fetchall()

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
    # 作为脚本直接运行时，按顺序执行：迁移 -> 写演示数据 -> 打印状态。
    apply_migrations()
    seed_user()
    print_state()
