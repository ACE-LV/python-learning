# 第八天练习题
# 主题：FastAPI + SQLite
from collections.abc import Iterator
from contextlib import closing, contextmanager
from datetime import datetime
from sqlite3 import Connection, Row

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from day08.main import get_conn

# 目标：在 day08/main.py 的基础上做二次练习。
app = FastAPI(title="Day08 Practice")


class UserCreateWithTimestamp(BaseModel):
    name: str
    role: str
    active: bool = True


def user_to_dict(row: Row) -> dict[str, object]:
    return {
        "id": row["id"],
        "name": row["name"],
        "role": row["role"],
        "active": bool(row["active"]),
    }


@contextmanager
def open_conn() -> Iterator[Connection]:
    with closing(get_conn()) as conn:
        with conn:
            yield conn


def init_practice_db() -> None:
    with open_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT
            )
            """
        )
        columns = conn.execute("PRAGMA table_info(users)").fetchall()
        column_names = {column["name"] for column in columns}
        if "created_at" not in column_names:
            conn.execute("ALTER TABLE users ADD COLUMN created_at TEXT")


@app.on_event("startup")
def on_startup() -> None:
    init_practice_db()


# 练习 1：实现 DELETE /users/{user_id}
# 要求：删除成功返回 {"ok": True}；找不到返回 404。
@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, bool]:
    with open_conn() as conn:
        cur = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}


# 练习 2：实现 PATCH /users/{user_id}/deactivate
# 要求：把 active 设为 0，返回更新后的用户。


@app.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: int) -> dict[str, object]:
    with open_conn() as conn:
        cur = conn.execute("UPDATE users SET active = 0 WHERE id = ?", (user_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        row = conn.execute(
            "SELECT id, name, role, active FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_to_dict(row)


# 练习 3：实现 GET /users?role=frontend
# 要求：支持可选 query 参数 role 做过滤。


@app.get("/users")
def get_users_by_role(role: str | None = None) -> list[dict[str, object]]:
    with open_conn() as conn:
        if role is None:
            rows = conn.execute(
                "SELECT id, name, role, active FROM users ORDER BY id"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, name, role, active FROM users WHERE role = ? ORDER BY id",
                (role,),
            ).fetchall()

    return [user_to_dict(row) for row in rows]


# 练习 4：实现 POST /seed
# 要求：插入 3 条测试数据，返回新增数量。


@app.post("/seed")
def seed_users() -> dict[str, int]:
    users = [
        {
            "name": f"User {i}",
            "role": "frontend" if i % 2 == 0 else "backend",
            "active": True,
        }
        for i in range(1, 4)
    ]
    with open_conn() as conn:
        cur = conn.executemany(
            "INSERT INTO users (name, role, active) VALUES (?, ?, ?)",
            [(user["name"], user["role"], int(user["active"])) for user in users],
        )
    return {"inserted": cur.rowcount}


# 练习 5（可选）：
# 新增字段 created_at，并在插入时写入当前时间。
@app.post("/users_with_timestamp")
def create_user_with_timestamp(payload: UserCreateWithTimestamp) -> dict[str, object]:
    created_at = datetime.now().isoformat()

    with open_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (name, role, active, created_at) VALUES (?, ?, ?, ?)",
            (payload.name, payload.role, int(payload.active), created_at),
        )
        user_id = int(cur.lastrowid)

    return {
        "id": user_id,
        "name": payload.name,
        "role": payload.role,
        "active": payload.active,
        "created_at": created_at,
    }