# 第六天练习题
# 主题：FastAPI 路由与请求体

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Day06 Practice")


class UserCreate(BaseModel):
    name: str
    role: str
    active: bool = True


users = [
    {"id": 1, "name": "Ace", "role": "frontend", "active": True},
    {"id": 2, "name": "Lily", "role": "backend", "active": True},
]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# 练习 1：实现 GET /users
# 要求：返回 users 列表。


@app.get("/users")
def get_users() -> list[dict[str, object]]:
    return users


# 练习 2：实现 GET /users/{user_id}
# 要求：返回单个用户；找不到则抛 404。
@app.get("/users/{user_id}")
def get_users_byId(user_id: int) -> dict[str, object]:
    for item in users:
        if item["id"] == user_id:
            return item
    raise HTTPException(status_code=404, detail="User not found")


# 练习 3：实现 POST /users
# 要求：
# - 使用 UserCreate 作为请求体
# - 自动生成新 id
# - append 到 users
# - 返回新用户


@app.post("/users")
def create_user(params: UserCreate) -> dict[str, object]:
    record = {
        "id": max([item["id"] for item in users], default=0) + 1,
        "name": params.name,
        "role": params.role,
        "active": params.active,
    }
    users.append(record)
    return record


# 练习 4：实现 GET /users/role/{role}
# 要求：返回指定 role 的用户列表。
@app.get("/users/role/{role}")
def get_users_by_role(role: str) -> list[dict[str, object]]:
    return [item for item in users if item["role"] == role]


# 练习 5（可选）：实现 PATCH /users/{user_id}/deactivate
# 要求：把目标用户 active 改成 False；找不到返回 404。
@app.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: int) -> dict[str, object]:
    for item in users:
        if item["id"] == user_id:
            item["active"] = False
            return item
    raise HTTPException(status_code=404, detail="User not found")
