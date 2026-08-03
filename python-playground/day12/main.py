from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# 第 12 天主题：给前端表格页提供标准查询接口。
# 前端表格常见需求：分页、搜索、筛选、排序，这些通常都通过 query 参数传给后端。
app = FastAPI(title="Day12 Pagination Search Sort")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day12_users.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Role 限制 role 查询参数和响应字段只能是固定角色值。
Role = Literal["frontend", "backend", "tester", "pm"]

# SortBy 限制前端只能按这些字段排序，避免传入任意字段名。
# 如果允许任意 sort_by，真实项目里可能带来 SQL 注入或无效字段问题。
SortBy = Literal["id", "name", "role"]

# SortOrder 限制排序方向只能是升序 asc 或降序 desc。
SortOrder = Literal["asc", "desc"]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class UserPublic(BaseModel):
    # 单个用户返回结构。
    # PageResult.items 会复用它，保证列表里每条数据结构稳定。
    id: int
    name: str
    role: Role
    active: bool


class PageResult(BaseModel):
    # 前端表格页常见响应结构。
    # items 是当前页数据，不是全部数据。
    items: list[UserPublic]
    # total 是过滤/搜索后的总条数。
    # 前端需要它来计算总页数和显示 “1-10 of 28 items”。
    total: int
    # page/page_size 回显当前请求参数，方便前端确认当前页状态。
    page: int
    page_size: int
    # total_pages 是后端算好的总页数；前端也可以用 total/page_size 自己算。
    total_pages: int


def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "active": user.active,
    }


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    # Seed demo data only once for learning.
    with Session(engine) as session:
        existing = session.scalar(select(User.id).limit(1))
        if existing is not None:
            return

        session.add_all(
            [
                User(name="Alice", role="frontend", active=True),
                User(name="Bob", role="backend", active=True),
                User(name="Cindy", role="tester", active=False),
                User(name="Daniel", role="frontend", active=True),
                User(name="Eva", role="pm", active=True),
                User(name="Frank", role="backend", active=False),
                User(name="Grace", role="frontend", active=True),
            ]
        )
        session.commit()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口，用于确认服务启动。
    return {"status": "ok"}


@app.get("/users", response_model=PageResult)
def list_users(
    # page 是当前页，从 1 开始。
    # ge=1 表示必须 >= 1；如果 page=0，FastAPI 自动返回 422。
    page: int = Query(default=1, ge=1),

    # page_size 是每页条数。
    # ge=1/le=50 限制最小 1、最大 50，避免前端一次请求太多数据。
    page_size: int = Query(default=5, ge=1, le=50),

    # keyword 是可选搜索词。
    # None 表示前端没传 keyword，不做搜索。
    keyword: str | None = Query(default=None),

    # role 是可选筛选条件，且只能是 Role 定义的合法值。
    role: Role | None = Query(default=None),

    # active 是可选布尔筛选条件。
    # URL 里可以传 active=true 或 active=false。
    active: bool | None = Query(default=None),

    # sort_by / sort_order 控制排序。
    # 默认按 id 升序，保证结果顺序稳定。
    sort_by: SortBy = Query(default="id"),
    sort_order: SortOrder = Query(default="asc"),
) -> dict[str, object]:
    conditions = []
    if keyword:
        lowered_keyword = keyword.lower()
        conditions.append(func.lower(User.name).contains(lowered_keyword))
    if role is not None:
        conditions.append(User.role == role)
    if active is not None:
        conditions.append(User.active == active)

    sort_mapping = {
        "id": User.id,
        "name": User.name,
        "role": User.role,
    }
    sort_column = sort_mapping[sort_by]
    ordered_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()

    start = (page - 1) * page_size

    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(User).where(*conditions)) or 0
        stmt = (
            select(User)
            .where(*conditions)
            .order_by(ordered_column)
            .offset(start)
            .limit(page_size)
        )
        rows = session.scalars(stmt).all()

    total_pages = (total + page_size - 1) // page_size if total else 0
    return {
        "items": [user_to_dict(user) for user in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
