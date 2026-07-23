# 第六天作业
# 主题：用户管理 API（FastAPI）

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Day06 Homework")


class UserCreate(BaseModel):
    name: str
    role: str
    active: bool = True


class UserUpdateRole(BaseModel):
    role: str


users = [
    {"id": 1, "name": "Ace", "role": "frontend", "active": True},
    {"id": 2, "name": "Lily", "role": "backend", "active": True},
    {"id": 3, "name": "Tom", "role": "qa", "active": False},
]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# 作业 1：实现 GET /users
# 返回全部用户。


@app.get("/users")
def get_users() -> list[dict[str, object]]:
    return users


# 作业 2：实现 GET /users/{user_id}
# 找不到返回 404。
@app.get("/users/{user_id}")
def get_user_by_id(user_id: int) -> dict[str, object]:
    for item in users:
        if item["id"] == user_id:
            return item
    raise HTTPException(status_code=404, detail="User not found")


# 作业 3：实现 POST /users
# 使用 UserCreate，新增并返回用户。
@app.post("/users")
def create_user(params: UserCreate) -> dict[str, object]:
    record = {
        "id": max([item["id"] for item in users], default=0) + 1,
        "name": params.name,
        "role": params.role,
        "active": params.active,
    }
    return record


# 作业 4：实现 PATCH /users/{user_id}/role
# 使用 UserUpdateRole 更新 role，找不到返回 404。
@app.patch("/users/{user_id}/role")
def update_user_role(user_id: int) -> dict[str, object]:
    for item in users:
        if item["id"] == user_id:
            ace = UserUpdateRole(role="aaa")
            item["role"] = ace.role
            return item
    raise HTTPException(status_code=404, detail="User not found")


# 作业 5：实现 GET /report
# 返回：
# - total
# - active_count
# - role_count
# - frontend_names


@app.get("/report")
def get_report() -> dict[str, object]:
    result = {
        "total": len(users),
        "active_count": len([item for item in users if item["active"]]),
        "role_count": count_by_role(users),
        "frontend_names": [
            item["name"] for item in users if item["role"] == "frontend"
        ],
    }
    return result


def count_by_role(users: list[dict[str, object]]) -> int:
    role = {}
    for item in users:
        role[item["role"]] = role.get(item["role"], 0) + 1
    return len(role)
