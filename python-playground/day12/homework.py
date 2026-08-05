# 第十二天作业
# 主题：设计一个前端表格页接口

# 作业要求：
# 1. 实现 GET /users。
# 2. 支持 page、page_size。
# 3. 支持 keyword 搜索 name。
# 4. 支持 role 筛选。
# 5. 支持 active 筛选。
# 6. 支持 sort_by、sort_order。
# 7. 返回 items、total、page、page_size、total_pages。
# 8. 在 summary.md 解释为什么 total 很重要。

from fastapi import FastAPI, Query
from sqlalchemy import func, select, create_engine
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase
from pydantic import BaseModel
from pathlib import Path
from typing import Literal

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day12_users.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

app = FastAPI(title="Day12 Homework User API", version="1.0.0")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SortBy = Literal["id", "name", "role", "active"]
SortOrder = Literal["asc", "desc"]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)


class UserResponse(BaseModel):
    id: int
    name: str
    role: str
    active: bool


class UserPageResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


def init_db():
    # 初始化数据库，创建 users 表并插入一些测试数据。
    with Session(engine) as session:
        Base.metadata.create_all(bind=engine)
        users_count = session.scalar(select(func.count()).select_from(User))
        if users_count == 0:
            # 如果 users 表为空，则插入测试数据
            session.add_all(
                [
                    User(name="Alice", role="frontend", active=True),
                    User(name="Bob", role="backend", active=True),
                    User(name="Charlie", role="tester", active=False),
                    User(name="David", role="pm", active=True),
                    User(name="Eve", role="frontend", active=False),
                ]
            )
            session.commit()


@app.on_event("startup")
def on_startup():
    init_db()


def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "active": user.active,
    }


@app.get("/users", response_model=UserPageResponse)
def get_users(
    keyword: str | None = Query(default=None, description="按用户名称搜索"),
    role: str | None = Query(default=None, description="用户角色"),
    active: bool | None = Query(default=None, description="是否启用"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=10, ge=1, le=100, description="每页数量"),
    sort_by: SortBy = Query(default="id", description="排序字段"),
    sort_order: SortOrder = Query(default="asc", description="排序顺序"),
) -> dict[str, object]:
    conditions = []
    if keyword:
        conditions.append(func.lower(User.name).contains(keyword.lower()))
    if role is not None:
        conditions.append(User.role == role)
    if active is not None:
        conditions.append(User.active == active)

    sort_mapping = {
        "id": User.id,
        "name": User.name,
        "role": User.role,
        "active": User.active,
    }
    sort_column = sort_mapping[sort_by]
    ordered_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()

    with Session(engine) as session:
        total = (
            session.scalar(select(func.count()).select_from(User).where(*conditions))
            or 0
        )
        total_pages = (total + page_size - 1) // page_size if total else 0
        offset = (page - 1) * page_size
        users = session.scalars(
            select(User)
            .where(*conditions)
            .order_by(ordered_column)
            .offset(offset)
            .limit(page_size)
        ).all()
        return {
            "items": [user_to_dict(user) for user in users],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
