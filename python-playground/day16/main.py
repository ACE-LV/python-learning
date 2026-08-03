from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# 第 16 天主题：给 FastAPI 接口写自动化测试。
# main.py 提供被测试的 API，test_main.py 使用 TestClient 模拟 HTTP 请求。
app = FastAPI(title="Day16 FastAPI Tests")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day16_users.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)


def user_to_dict(user: User) -> dict[str, object]:
    return {"id": user.id, "name": user.name, "role": user.role}


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    # POST /users 的请求体。
    # Field 约束可以被测试覆盖：空 name 会返回 422。
    name: str = Field(min_length=1, max_length=50)
    role: str = Field(min_length=1, max_length=50)


def reset_users() -> None:
    # 重置测试数据。
    # 为什么需要：每个测试都应该独立运行，不依赖上一个测试新增/删除后的状态。
    # pytest fixture 会在每个测试前调用它。
    with Session(engine) as session:
        session.query(User).delete()
        session.add(User(id=1, name="Alice", role="frontend"))
        session.commit()


def find_user(user_id: int) -> dict[str, object] | None:
    # 根据 id 查找用户，找不到返回 None。
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            return None
        return user_to_dict(user)


# 模块加载时先初始化一次数据，方便手动运行服务时也有默认用户。
init_db()
reset_users()


@app.get("/health")
def health_check() -> dict[str, str]:
    # 用于测试服务是否能正常响应。
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict[str, object]]:
    # 返回当前所有用户。测试会断言初始数据只有 Alice。
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [user_to_dict(user) for user in users]


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    # 成功场景返回用户；失败场景返回 404。
    # 自动化测试需要覆盖这两种情况。
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    # 创建用户接口。
    # 测试会覆盖合法 payload 返回 200，以及非法 payload 返回 422。
    with Session(engine) as session:
        user = User(name=payload.name, role=payload.role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user_to_dict(user)
