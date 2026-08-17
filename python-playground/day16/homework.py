# 第十六天作业
# 主题：给用户 API 补测试

# 作业要求：
# 1. 为 GET /health 写测试。
# 2. 为 GET /users 写测试。
# 3. 为 POST /users 写测试。
# 4. 为 GET /users/{id} 成功场景写测试。
# 5. 为 GET /users/{id} 404 场景写测试。
# 6. 为 POST /users 422 场景写测试。
# 7. 使用 fixture 重置测试数据。
# 8. 在 summary.md 写清楚手动测试和自动化测试的区别。
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Mapped, Session, mapped_column, DeclarativeBase
from pathlib import Path
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day16_homework.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

app = FastAPI(title="Day16 Homework Test API")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class UserCreate(BaseModel):
    name: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: int
    name: str


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def reset_users() -> None:
    init_db()
    with Session(engine) as session:
        session.query(User).delete()
        session.add_all(
            [
                User(id=1, name="Alice"),
                User(id=2, name="Bob"),
            ]
        )
        session.commit()


@app.on_event("startup")
def startup_event():
    reset_users()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users", response_model=list[UserResponse])
def get_users():
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [UserResponse(id=user.id, name=user.name) for user in users]


@app.post("/users")
def create_user(user: UserCreate):
    with Session(engine) as session:
        new_user = User(name=user.name)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserResponse(id=new_user.id, name=new_user.name)


@app.get("/users/{user_id}")
def get_user(user_id: int) -> UserResponse | None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=user.id, name=user.name)


@pytest.fixture()
def client() -> TestClient:
    reset_users()
    return TestClient(app)


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_users(client: TestClient):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]


def test_get_user_success(client: TestClient):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice"}


def test_create_user(client: TestClient):
    response = client.post("/users", json={"name": "Charlie"})
    assert response.status_code == 200
    assert response.json()["name"] == "Charlie"


def test_get_user_not_found(client: TestClient):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_invalid(client: TestClient):
    response = client.post("/users", json={"name": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"
