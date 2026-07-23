from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI 应用实例，后续所有路由都挂在 app 上。
app = FastAPI(title="Day06 FastAPI Demo")


# Pydantic 模型：用于校验 POST 请求体。
class UserCreate(BaseModel):
    name: str
    role: str
    active: bool = True


# 用列表模拟“内存数据库”，先理解 API 流程，后续再接真实数据库。
users = [
    {"id": 1, "name": "Ace", "role": "frontend", "active": True},
    {"id": 2, "name": "Lily", "role": "backend", "active": True},
]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict[str, object]]:
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    new_id = max([item["id"] for item in users], default=0) + 1
    user = {
        "id": new_id,
        "name": payload.name,
        "role": payload.role,
        "active": payload.active,
    }
    users.append(user)
    return user
