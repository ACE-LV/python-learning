# 第九天练习题
# 主题：SQLAlchemy ORM
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

base_dir = Path(__file__).resolve().parent  # 当前 Python 文件所在的文件夹
db_path = base_dir / "day09.db"  # SQLite 数据库文件，保存在当前 Python 文件所在的文件夹
base_url = f"sqlite:///{db_path}"  # 数据库连接 URL


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
    email: Mapped[str] = mapped_column(String(120), nullable=True)  # 用户邮箱，选填


app = FastAPI(title="Day09 SQLAlchemy ORM")  # FastAPI 应用实例
engine = create_engine(base_url, echo=True, future=True)  # 数据库引擎


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# 练习 1：在 User 模型上新增 email 字段。
# 提示：新增 mapped_column(String(120), nullable=True)。


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# 练习 2：修改 POST /users，让它能保存 email。
@app.post("/users")
def create_user(user: User) -> dict[str, object]:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "active": user.active,
            "email": user.email,
        }


# 练习 3：实现 DELETE /users/{user_id}。
# 要求：删除成功返回 {"ok": True}；找不到返回 404。
@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, bool]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}


# 练习 4：实现 GET /users?role=frontend。
# 要求：role 是可选 query 参数，有值时按角色过滤。


@app.get("/users")
def list_users(role: str | None = None) -> list[dict[str, object]]:
    with Session(engine) as session:
        query = session.query(User)
        if role:
            query = query.filter(User.role == role)
        users = query.all()
        return [
            {
                "id": user.id,
                "name": user.name,
                "role": user.role,
                "active": user.active,
                "email": user.email,
            }
            for user in users
        ]


# 练习 5：实现 PATCH /users/{user_id}/deactivate。
# 要求：把 active 改成 False，并返回更新后的用户。

@app.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: int) -> dict[str, object]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.active = False
        session.commit()
        return {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "active": user.active,
            "email": user.email,
        }