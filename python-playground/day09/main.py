from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day09_users.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
app = FastAPI(title="Day09 SQLAlchemy ORM")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class UserCreate(BaseModel):
    name: str
    role: str
    active: bool = True


class UserUpdateRole(BaseModel):
    role: str


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
def list_users() -> list[dict[str, object]]:
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [user_to_dict(user) for user in users]


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user_to_dict(user)


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
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
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.role = payload.role
        session.commit()
        session.refresh(user)
        return user_to_dict(user)
