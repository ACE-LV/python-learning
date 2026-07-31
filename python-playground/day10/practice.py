# 第十天练习题
# 主题：Pydantic 校验与 response_model

# 练习 1：给 UserCreate 新增 email 字段。
# 要求：先用普通 str，不要引入额外依赖。

# 练习 2：给 UserCreate 新增 level 字段。
# 要求：只能是 "junior"、"middle"、"senior"。

# 练习 3：实现 GET /users?role=frontend。
# 要求：role 可选，有值时过滤用户。

# 练习 4：新增 UserPrivate 模型。
# 要求：模拟内部字段 password_hash，但不要通过 response_model 返回。

# 练习 5：故意提交非法 age，观察 /docs 里的 422 响应。

from typing import Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, select
from fastapi.responses import JSONResponse
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from pathlib import Path

base_dir = Path(__file__).resolve().parent
db_dir = base_dir / "day10_users.db"
db_url = f"sqlite:///{db_dir.as_posix()}"

engine = create_engine(db_url, connect_args={"check_same_thread": False})
app = FastAPI(title="Day10 Pydantic Validation")
app.on_event("startup")(lambda: User.metadata.create_all(bind=engine))
session = Session(engine)
role = Literal["frontend", "backend", "tester", "pm"]
level = Literal["junior", "middle", "senior"]


class User(DeclarativeBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)  # 练习 1
    role: Mapped[role] = mapped_column(nullable=False)  # 练习 2
    level: Mapped[level] = mapped_column(nullable=False)  # 练习 2


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=5, max_length=100)  # 练习 1
    role: role
    level: level


class response_model(BaseModel):
    id: int
    name: str
    email: str
    role: role
    level: level
class UserPrivate (BaseModel):
    id: int
    name: str
    email: str
    role: role
    level: level
    password_hash: str  # 练习 4

def response_model(user: User) -> response_model:
    return response_model(
        id=user.id, name=user.name, email=user.email, role=user.role, level=user.level
    )


@app.patch("/users/{user_id}")
def update_user_by_id(user_id: int, user: UserCreate) -> dict[response_model]:
    with session.begin():
        db_user = session.get(User, user_id)
        if not db_user:
            return JSONResponse(status_code=404, content={"message": "User not found"})
        db_user.name = user.name
        db_user.email = user.email
        db_user.role = user.role
        db_user.level = user.level
    return response_model(db_user)


@app.get("/users/{role}")
def get_user_by_role(role: role | None = Query(None)) -> list[response_model]:
    with session.begin():
        if role:
            user = session.scalars(select(User).where(User.role == role)).all()
        else:
            user = session.scalars(select(User)).all()
    return [response_model(u) for u in user]
