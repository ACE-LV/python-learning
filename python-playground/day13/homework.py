# 第十三天作业
# 主题：给接口加最小鉴权

# 作业要求：
# 1. 保留一个公开健康检查接口。
# 2. 新增 require_token 依赖函数。
# 3. 从 Authorization 请求头读取 Bearer token。
# 4. token 错误或缺失时返回 401。
# 5. 给 /me、/notes、/admin/users 加鉴权。
# 6. 在 summary.md 写清楚 401、403、404 的区别。

from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day13_auth.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"
app = FastAPI(title="Day13 Homework Depends Auth")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
API_TOKEN = "dev-token"
ADMIN_TOKEN = "admin-token"


@app.on_event("startup")
def init_db():
    # 初始化数据库，创建表。
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.scalar(select(User.id).limit(1)) is None:
            # 插入一些测试数据。
            session.add_all(
                [
                    User(name="Alice", role="admin"),
                    User(name="Bob", role="user"),
                    User(name="Charlie", role="user"),
                ]
            )
            session.commit()
        if session.scalar(select(Note.id).limit(1)) is None:
            session.add_all(
                [
                    Note(title="Note 1", content="Content 1"),
                    Note(title="Note 2", content="Content 2"),
                ]
            )
            session.commit()


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


class UserResponse(BaseModel):
    id: int
    name: str
    role: str


class NoteResponse(BaseModel):
    id: int
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


def require_token(authorization: str | None = Header(None)) -> None:
    expected_token = f"Bearer {API_TOKEN}"
    if authorization != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )


def require_admin_token(authorization: str | None = Header(None)) -> None:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    expected_token = f"Bearer {ADMIN_TOKEN}"
    if authorization != expected_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin permission required"
        )


@app.get("/health", summary="健康检查接口", description="公开接口，无需鉴权")
def health():
    return {"status": "ok"}


@app.get(
    "/me",
    response_model=UserResponse,
    summary="获取当前用户信息",
    description="需要鉴权，返回当前用户信息",
)
def get_me(_: None = Depends(require_token)) -> dict[str, object]:
    with Session(engine) as session:
        # 学习阶段简化：当前用户固定取第一条；真实项目应从 token/session 解析用户身份。
        user = session.scalar(select(User).order_by(User.id).limit(1))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_to_dict(user)


@app.get(
    "/notes",
    response_model=list[NoteResponse],
    summary="获取所有笔记",
    description="需要鉴权，返回所有笔记",
)
def get_notes(_: None = Depends(require_token)) -> list[dict[str, object]]:
    with Session(engine) as session:
        notes = session.scalars(select(Note).order_by(Note.id)).all()
        return [note_to_dict(note) for note in notes]


@app.get(
    "/admin/users",
    response_model=list[UserResponse],
    summary="获取所有用户",
    description="需要管理员权限，返回所有用户",
)
def get_admin_users(_: None = Depends(require_admin_token)) -> list[dict[str, object]]:
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [user_to_dict(user) for user in users]
