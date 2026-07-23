import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 当前文件所在目录，用来拼接数据库文件路径。
BASE_DIR = Path(__file__).resolve().parent
# SQLite 数据库文件：第一次运行会自动创建。
DB_PATH = BASE_DIR / "day08_users.db"

# FastAPI 应用实例。
app = FastAPI(title="Day08 FastAPI + SQLite")


# 请求体模型：用于 POST /users 参数校验。
class UserCreate(BaseModel):
    name: str
    role: str
    active: bool = True


# 请求体模型：用于 PATCH /users/{id}/role 的更新参数。
class UserUpdateRole(BaseModel):
    role: str


def get_conn() -> sqlite3.Connection:
    # 每次请求按需创建连接，避免全局连接长期占用。
    conn = sqlite3.connect(DB_PATH)
    # 启用按列名访问（row["id"]），而不是只能用下标 row[0]。
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    # 建表语句：如果 users 表不存在就创建。
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
            """
        )


@app.on_event("startup")
def on_startup() -> None:
    # 应用启动时执行一次，确保数据库表可用。
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口：常用于探活。
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict[str, object]]:
    # 查询全部用户，按 id 升序返回。
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name, role, active FROM users ORDER BY id").fetchall()

    # SQLite 里 active 存的是 0/1，返回前转成 True/False。
    return [
        {"id": row["id"], "name": row["name"], "role": row["role"], "active": bool(row["active"])}
        for row in rows
    ]


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    # 路径参数 user_id 自动按 int 校验。
    with get_conn() as conn:
        row = conn.execute("SELECT id, name, role, active FROM users WHERE id = ?", (user_id,)).fetchone()

    # 找不到资源返回 404。
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": row["id"], "name": row["name"], "role": row["role"], "active": bool(row["active"])}


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    # payload 来自请求体，Pydantic 会自动做字段与类型校验。
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (name, role, active) VALUES (?, ?, ?)",
            (payload.name, payload.role, int(payload.active)),
        )
        # SQLite 自增主键 id。
        user_id = int(cur.lastrowid)

    return {"id": user_id, "name": payload.name, "role": payload.role, "active": payload.active}


@app.patch("/users/{user_id}/role")
def update_user_role(user_id: int, payload: UserUpdateRole) -> dict[str, object]:
    # PATCH：部分更新，这里只更新 role 字段。
    with get_conn() as conn:
        cur = conn.execute("UPDATE users SET role = ? WHERE id = ?", (payload.role, user_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        row = conn.execute("SELECT id, name, role, active FROM users WHERE id = ?", (user_id,)).fetchone()

    return {"id": row["id"], "name": row["name"], "role": row["role"], "active": bool(row["active"])}


@app.get("/report")
def get_report() -> dict[str, object]:
    # 报表接口：演示 SQL 聚合统计。
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
        active_count = conn.execute("SELECT COUNT(*) AS c FROM users WHERE active = 1").fetchone()["c"]
        role_rows = conn.execute("SELECT role, COUNT(*) AS c FROM users GROUP BY role").fetchall()
        frontend_rows = conn.execute("SELECT name FROM users WHERE role = 'frontend'").fetchall()

    # 把 SQL 结果转换成前端更好用的结构。
    role_count = {row["role"]: row["c"] for row in role_rows}
    frontend_names = [row["name"] for row in frontend_rows]

    return {
        "total": total,
        "active_count": active_count,
        "role_count": role_count,
        "frontend_names": frontend_names,
    }
