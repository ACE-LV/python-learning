# 第八天作业
# 主题：用户管理持久化 API

# 作业要求：
# 1. 建立 users 表（id, name, role, active）。
# 2. 完成 GET /users。
# 3. 完成 POST /users。
# 4. 完成 PATCH /users/{id}/role。
# 5. 完成 GET /report。
# 6. 所有找不到资源的场景返回 404。
# 7. 代码可在 /docs 完整联调。

# 建议直接基于 day08/main.py 复制一份独立实现。

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from sqlite3 import Connection, connect

base_dir = Path(__file__).resolve().parent
db_path = base_dir / "day08_users.db"



class UserCreate(BaseModel):
    name: str
    role: str
    active: bool = True


def init_db() -> None:
    # 当前文件所在目录，用来拼接数据库文件路径。
    # SQLite 数据库文件：第一次运行会自动创建。
    # 建表语句：如果 users 表不存在就创建。
    with connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
            """)


app = FastAPI(title="Day08 Homework")


@app.on_event("startup")
def on_startup() -> None:
    # 应用启动时执行一次，确保数据库表可用。
    init_db()
  


def connect_db() -> Connection:
    # 每次请求按需创建连接，避免全局连接长期占用。
    conn = connect(db_path)
    # 启用按列名访问（row["id"]），而不是只能用下标 row[0]。
    conn.row_factory = lambda cursor, row: {
        col[0]: row[idx] for idx, col in enumerate(cursor.description)
    }
    return conn


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口：常用于探活。
    return {"status": "ok"}


# 完成 GET /users
@app.get("/users")
def get_users() -> list[dict[str, object]]:
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM users").fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No users found")
        return rows


# 完成 POST /users
@app.post("/users")
def create_user(user: UserCreate) -> dict[str, object]:
    with connect_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name, role, active) VALUES (?, ?, ?)",
            (user.name, user.role, int(user.active)),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=500, detail="Failed to create user")
        user_id = cursor.lastrowid
        return {
            "id": user_id,
            "name": user.name,
            "role": user.role,
            "active": user.active,
        }


# 完成 PATCH /users/{id}/role
@app.patch("/users/{user_id}/role")
def update_user_role(user_id: int, user: UserCreate) -> dict[str, object]:
    with connect_db() as conn:
        cursor = conn.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (user.role, user_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return row


# 完成 GET /report。
@app.get("/report")
def get_report() -> dict[str, int]:
    with connect_db() as conn:
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active_users = conn.execute(
            "SELECT COUNT(*) FROM users WHERE active = 1"
        ).fetchone()[0]
        inactive_users = conn.execute(
            "SELECT COUNT(*) FROM users WHERE active = 0"
        ).fetchone()[0]
        if total_users == 0:
            raise HTTPException(status_code=404, detail="No users found")
        if active_users == 0:
            raise HTTPException(status_code=404, detail="No active users found")
        if inactive_users == 0:
            raise HTTPException(status_code=404, detail="No inactive users found")
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
        }

