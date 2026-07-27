from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Day10 Pydantic Validation")

Role = Literal["frontend", "backend", "tester", "pm"]


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    role: Role
    age: int = Field(ge=1, le=120)
    active: bool = True


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    role: Role | None = None
    age: int | None = Field(default=None, ge=1, le=120)
    active: bool | None = None


class UserPublic(BaseModel):
    id: int
    name: str
    role: Role
    age: int
    active: bool


USERS: list[dict[str, object]] = [
    {"id": 1, "name": "Alice", "role": "frontend", "age": 28, "active": True},
    {"id": 2, "name": "Bob", "role": "backend", "age": 32, "active": True},
]
NEXT_ID = 3


def find_user(user_id: int) -> dict[str, object] | None:
    return next((user for user in USERS if user["id"] == user_id), None)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users", response_model=list[UserPublic])
def list_users(active: bool | None = Query(default=None)) -> list[dict[str, object]]:
    if active is None:
        return USERS
    return [user for user in USERS if user["active"] is active]


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
