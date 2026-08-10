# 第十三天练习题
# 主题：Depends 与简单 token 鉴权

# 练习 1：把 API_TOKEN 改成从环境变量读取。
# 提示：使用 os.getenv("API_TOKEN", "dev-token")。

# 练习 2：新增公开接口 GET /public/version。

# 练习 3：新增受保护接口 DELETE /notes/{note_id}。
# 要求：缺 token 返回 401，找不到 note 返回 404。

# 练习 4：新增 require_admin_token。
# 要求：只有 Authorization: Bearer admin-token 可以访问 /admin/users。

# 练习 5：在 /docs 里分别测试有 token 和无 token 的请求。


from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day13_auth.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"
app = FastAPI(title="Day13 Practice Depends Auth")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)


API_TOKEN = os.getenv("API_TOKEN", "dev-token")


class UserPublic(BaseModel):
    id: int
    name: str
    role: str


class NoteCreate(BaseModel):
    title: str
    content: str


def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
    }


def note_to_dict(note: Note) -> dict[str, object]:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
    }


def require_token(authorization: str | None = Header(default=None)) -> None:
    expected_token = f"Bearer {API_TOKEN}"
    if authorization != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )


def require_admin_token(authorization: str | None = Header(default=None)) -> None:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    if authorization != "Bearer admin-token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required",
        )


@app.get("/public/version")
def get_version() -> dict[str, str]:
    return {"version": "1.0.0"}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, _: None = Depends(require_token)) -> dict[str, str]:
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )
        session.delete(note)
        session.commit()
        return {"status": "deleted"}


@app.get("/admin/users", response_model=list[UserPublic])
def get_admin_users(_: None = Depends(require_admin_token)) -> list[dict[str, object]]:
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [user_to_dict(user) for user in users]


@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        # 初始化测试数据。
        if session.scalar(select(User.id).limit(1)) is None:
            session.add_all(
                [
                    User(id=1, name="Alice", role="frontend"),
                    User(id=2, name="Bob", role="backend"),
                    User(id=3, name="Charlie", role="admin"),
                ]
            )
            session.commit()
        if session.scalar(select(Note.id).limit(1)) is None:
            session.add_all(
                [
                    Note(title="First note", content="Hello day13"),
                    Note(title="Second note", content="Practice delete"),
                ]
            )
            session.commit()
