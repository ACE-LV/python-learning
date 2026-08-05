# # 第十二天练习题
# # 主题：分页、搜索、排序

# # 练习 1：给 /users 增加 active 可选筛选。
# # 练习 2：把 page_size 最大值从 50 改成 20，观察 /docs 变化。
# # 练习 3：新增 sort_by="active" 支持。
# # 练习 4：新增 GET /users/simple。
# # 练习 5：当 page 超过 total_pages 时返回空 items。

# from datetime import datetime
# from pathlib import Path
# from typing import Literal

# from fastapi import FastAPI, Query
# from pydantic import BaseModel
# from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, func, select
# from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# BASE_DIR = Path(__file__).resolve().parent
# DB_PATH = BASE_DIR / "day12_practice_users.db"
# DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

# app = FastAPI(title="Day12 Practice User API", version="1.0.0")
# engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# SortBy = Literal["name", "email", "active"]


# class Base(DeclarativeBase):
#     pass


# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
#     email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
#     active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# class UserResponse(BaseModel):
#     id: int
#     name: str
#     email: str
#     active: bool
#     created_at: datetime


# def user_to_dict(user: User) -> dict[str, object]:
#     return {
#         "id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "active": user.active,
#         "created_at": user.created_at,
#     }


# def init_db() -> None:
#     Base.metadata.create_all(bind=engine)

#     with Session(engine) as session:
#         existing = session.scalar(select(User.id).limit(1))
#         if existing is not None:
#             return

#         session.add_all(
#             [
#                 User(name="Alice", email="alice@example.com", active=True),
#                 User(name="Bob", email="bob@example.com", active=True),
#                 User(name="Cindy", email="cindy@example.com", active=False),
#                 User(name="Daniel", email="daniel@example.com", active=True),
#                 User(name="Eva", email="eva@example.com", active=False),
#             ]
#         )
#         session.commit()


# @app.on_event("startup")
# def on_startup() -> None:
#     init_db()


# @app.get("/users", response_model=list[UserResponse])
# def get_users(
#     page: int = Query(1, ge=1),
#     page_size: int = Query(20, ge=1, le=20),
#     active: bool | None = Query(None),
#     sort_by: SortBy | None = Query(None),
# ) -> list[dict[str, object]]:
#     conditions = []
#     if active is not None:
#         conditions.append(User.active == active)

#     sort_mapping = {
#         "name": User.name,
#         "email": User.email,
#         "active": User.active,
#     }

#     stmt = select(User).where(*conditions)
#     if sort_by is not None:
#         stmt = stmt.order_by(sort_mapping[sort_by])
#     else:
#         stmt = stmt.order_by(User.id)

#     total = 0
#     offset = (page - 1) * page_size

#     with Session(engine) as session:
#         total = session.scalar(select(func.count()).select_from(User).where(*conditions)) or 0
#         total_pages = (total + page_size - 1) // page_size if total else 0
#         if page > total_pages and total_pages > 0:
#             return []

#         users = session.scalars(stmt.offset(offset).limit(page_size)).all()
#         return [user_to_dict(user) for user in users]


# @app.get("/users/simple", response_model=list[UserResponse])
# def get_users_simple() -> list[dict[str, object]]:
#     with Session(engine) as session:
#         users = session.scalars(select(User).order_by(User.id)).all()
#         return [user_to_dict(user) for user in users]


from fastapi import FastAPI, Query
from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day12_practice_users.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

app = FastAPI(title="Day12 Practice User API", version="1.0.0")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

@app.on_event("startup")
def on_startup() -> None:
    init_db()
    
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = (mapped_column(Integer, primary_key=True, index=True),)
    name: Mapped[str] = (mapped_column(String(50), nullable=False, index=True),)
    email: Mapped[str] = (
        mapped_column(String(100), nullable=False, unique=True, index=True),
    )
    active: Mapped[bool] = (mapped_column(Boolean, default=True, nullable=False),)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
class UserResponse(BaseModel):
    items: list[dict[str, object]]
    total: int
    page: int
    page_size: int
    total_pages: int

def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "active": user.active,
        "created_at": user.created_at,
    }

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        existing = session.scalar(select(User.id).limit(1))
        if existing is not None:
            return

        session.add_all(
            [
                User(name="Alice", email="alice@example.com", active=True),
                User(name="Bob", email="bob@example.com", active=True),
                User(name="Cindy", email="cindy@example.com", active=False),
                User(name="Daniel", email="daniel@example.com", active=True),
                User(name="Eva", email="eva@example.com", active=False),
            ]
        )
        session.commit()

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get('/users',response_model=UserResponse)
def get_users(
    userId: int = Query(..., ge=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=20),
    active: bool | None = Query(None),
)->list[UserResponse]:
    sql=[]
    if active is not None:
        sql.append(User.active==active)
    if userId is not None:
        sql.append(User.id==userId)

    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(User).where(*sql)) or 0
        total_pages = (total // page_size) + (1 if total % page_size > 0 else 0)
        if page > total_pages and total_pages > 0:
            return []
        
        offset = (page - 1) * page_size
        users = session.scalars(select(User).where(*sql).offset(offset).limit(page_size)).all()
        return {
            'items':[user_to_dict(user) for user in users],
            'total':total,  
            'page':page,
            'page_size':page_size,
            'total_pages':total_pages
        }
    
        