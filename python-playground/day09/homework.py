# 第九天作业
# 主题：把 sqlite3 API 改造成 SQLAlchemy ORM API

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from sqlalchemy import Boolean, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

base_dir = Path(__file__).resolve().parent  # 当前 Python 文件所在的文件夹
db_path = base_dir / "day09_users.db"  # SQLite 数据库文件
db_url = f"sqlite:///{db_path.as_posix()}"  # 数据库连接 URL


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"  # 数据库表名

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )  # 主键，自增用户 ID
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # 用户显示名称，必填
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # 用户角色名称，必填
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )  # 用户是否启用


class UserCreate(BaseModel):
    name: str  # 用户显示名称，必填
    role: str  # 用户角色名称，必填
    active: bool = True  # 用户是否启用，默认启用


class UserUpdateRole(BaseModel):
    role: str  # 新的用户角色名称


app = FastAPI(title="Day09 SQLAlchemy ORM")  # FastAPI 应用实例
engine = create_engine(db_url, connect_args={"check_same_thread": False})  # 数据库引擎


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "active": user.active,
    }


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def get_users() -> list[dict[str, object]]:
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [user_to_dict(user) for user in users]


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user_to_dict(user)


@app.post("/users")
def create_users(payload: UserCreate) -> dict[str, object]:
    with Session(engine) as session:
        user = User(name=payload.name, role=payload.role, active=payload.active)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user_to_dict(user)


@app.patch("/users/{user_id}/role")
def update_user_role(user_id: int, payload: UserUpdateRole) -> dict[str, object]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = payload.role
        session.commit()
        session.refresh(user)
        return user_to_dict(user)


@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, bool]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}

# 作业要求：
# 1. 建立 User ORM 模型，字段包含 id、name、role、active。
# 2. 完成 GET /users。
# 3. 完成 GET /users/{user_id}。
# 4. 完成 POST /users。
# 5. 完成 PATCH /users/{user_id}/role。
# 6. 完成 DELETE /users/{user_id}。
# 7. 所有找不到用户的场景返回 404。
# 8. 在 summary.md 写清楚 ORM 和手写 SQL 的区别。
