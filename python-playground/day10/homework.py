# 第十天作业
# 主题：为用户接口补齐请求和响应模型

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Day10 Homework")

Role = Literal["frontend", "backend", "tester", "pm"]


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=1, le=120)
    role: Role


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    age: int | None = Field(default=None, ge=1, le=120)
    role: Role | None = None


class UserPublic(BaseModel):
    id: int
    name: str
    age: int
    role: Role


USERS: list[dict[str, object]] = [
    {"id": 1, "name": "Alice", "age": 28, "role": "frontend"},
    {"id": 2, "name": "Bob", "age": 32, "role": "backend"},
]
NEXT_ID = 3


def find_user(user_id: int) -> dict[str, object] | None:
    return next((user for user in USERS if user["id"] == user_id), None)


@app.get("/users", response_model=list[UserPublic])
def list_users() -> list[dict[str, object]]:
    return USERS


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int) -> dict[str, object]:
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=UserPublic)
def create_user(payload: UserCreate) -> dict[str, object]:
    global NEXT_ID

    user = {"id": NEXT_ID, **payload.dict()}
    USERS.append(user)
    NEXT_ID += 1
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, payload: UserUpdate) -> dict[str, object]:
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in payload.dict(exclude_none=True).items():
        user[key] = value
    return user
