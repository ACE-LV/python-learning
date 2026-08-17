# 第十六天练习题
# 主题：FastAPI 自动化测试

# 练习 1：新增 DELETE /users/{user_id}。

# 练习 2：为删除成功写测试。

# 练习 3：为删除不存在用户写 404 测试。

# 练习 4：新增 PATCH /users/{user_id}/role。

# 练习 5：为 PATCH 成功和失败分别写测试。

# 检查点：每个测试都应该能单独运行，不依赖上一个测试留下的数据。

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day16_test.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

app = FastAPI(title="Day16 Practice Test API")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)


class UserCreate(BaseModel):
    name: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    role: str


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.query(User).count() == 0:
            session.add_all(
                [
                    User(name="Alice", role="frontend"),
                    User(name="Bob", role="backend"),
                ]
            )
            session.commit()


@app.on_event("startup")
def startup_event():
    init_db()


@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        response = UserResponse(id=user.id, name=user.name, role=user.role)
        session.delete(user)
        session.commit()
        return response


@app.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int, role: str):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = role
        session.commit()
        session.refresh(user)
        return UserResponse(id=user.id, name=user.name, role=user.role)


def reset_users() -> None:
    init_db()
    with Session(engine) as session:
        session.query(User).delete()
        session.add_all(
            [
                User(id=1, name="Alice", role="frontend"),
                User(id=2, name="Bob", role="backend"),
            ]
        )
        session.commit()


import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    reset_users()
    return TestClient(app)


# 为删除成功写测试。
def test_delete_user_success(client: TestClient):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "role": "frontend"}


# 为删除失败写测试。
def test_delete_user_not_found(client: TestClient):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_role_success(client: TestClient):
    response = client.patch("/users/1/role", params={"role": "fullstack"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "role": "fullstack"}


def test_update_user_role_not_found(client: TestClient):
    response = client.patch("/users/999/role", params={"role": "fullstack"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
