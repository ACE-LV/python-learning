from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Day12 Pagination Search Sort")

Role = Literal["frontend", "backend", "tester", "pm"]
SortBy = Literal["id", "name", "role"]
SortOrder = Literal["asc", "desc"]


class UserPublic(BaseModel):
    id: int
    name: str
    role: Role
    active: bool


class PageResult(BaseModel):
    items: list[UserPublic]
    total: int
    page: int
    page_size: int
    total_pages: int


USERS: list[dict[str, object]] = [
    {"id": 1, "name": "Alice", "role": "frontend", "active": True},
    {"id": 2, "name": "Bob", "role": "backend", "active": True},
    {"id": 3, "name": "Cindy", "role": "tester", "active": False},
    {"id": 4, "name": "Daniel", "role": "frontend", "active": True},
    {"id": 5, "name": "Eva", "role": "pm", "active": True},
    {"id": 6, "name": "Frank", "role": "backend", "active": False},
    {"id": 7, "name": "Grace", "role": "frontend", "active": True},
]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users", response_model=PageResult)
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
    keyword: str | None = Query(default=None),
    role: Role | None = Query(default=None),
    active: bool | None = Query(default=None),
    sort_by: SortBy = Query(default="id"),
    sort_order: SortOrder = Query(default="asc"),
) -> dict[str, object]:
    rows = USERS.copy()

    if keyword:
        lowered_keyword = keyword.lower()
        rows = [user for user in rows if lowered_keyword in str(user["name"]).lower()]

    if role is not None:
        rows = [user for user in rows if user["role"] == role]

    if active is not None:
        rows = [user for user in rows if user["active"] is active]

    rows.sort(key=lambda user: user[sort_by], reverse=sort_order == "desc")

    total = len(rows)
    start = (page - 1) * page_size
    end = start + page_size
    items = rows[start:end]
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
