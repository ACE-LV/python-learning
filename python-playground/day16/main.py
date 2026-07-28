from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Day16 FastAPI Tests")

USERS: list[dict[str, object]] = []
NEXT_ID = 1


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    role: str = Field(min_length=1, max_length=50)


def reset_users() -> None:
    global NEXT_ID, USERS

    USERS = [{"id": 1, "name": "Alice", "role": "frontend"}]
    NEXT_ID = 2


def find_user(user_id: int) -> dict[str, object] | None:
    return next((user for user in USERS if user["id"] == user_id), None)


reset_users()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict[str, object]]:
    return USERS


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    global NEXT_ID

    user = {"id": NEXT_ID, "name": payload.name, "role": payload.role}
    USERS.append(user)
    NEXT_ID += 1
    return user
