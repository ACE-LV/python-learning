from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day18_tasks.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
app = FastAPI(title="Day18 Learning Task Tracker")

TaskStatus = Literal["todo", "doing", "done"]


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    owner: Mapped[str] = mapped_column(String(50), nullable=False)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    owner: str = Field(min_length=1, max_length=50)
    priority: int = Field(default=3, ge=1, le=5)


class TaskUpdateStatus(BaseModel):
    status: TaskStatus


class TaskPublic(BaseModel):
    id: int
    title: str
    status: TaskStatus
    priority: int
    owner: str


class ReportPublic(BaseModel):
    total: int
    status_count: dict[str, int]
    owner_count: dict[str, int]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def task_to_dict(task: Task) -> dict[str, object]:
    return {
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "priority": task.priority,
        "owner": task.owner,
    }


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskPublic)
def create_task(payload: TaskCreate) -> dict[str, object]:
    with Session(engine) as session:
        task = Task(title=payload.title, owner=payload.owner, priority=payload.priority)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task_to_dict(task)


@app.get("/tasks", response_model=list[TaskPublic])
def list_tasks(
    status: TaskStatus | None = Query(default=None),
    owner: str | None = Query(default=None),
) -> list[dict[str, object]]:
    stmt = select(Task).order_by(Task.priority, Task.id)
    if status is not None:
        stmt = stmt.where(Task.status == status)
    if owner is not None:
        stmt = stmt.where(Task.owner == owner)

    with Session(engine) as session:
        tasks = session.scalars(stmt).all()
        return [task_to_dict(task) for task in tasks]


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(task_id: int) -> dict[str, object]:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task_to_dict(task)


@app.patch("/tasks/{task_id}/status", response_model=TaskPublic)
def update_task_status(task_id: int, payload: TaskUpdateStatus) -> dict[str, object]:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task.status = payload.status
        session.commit()
        session.refresh(task)
        return task_to_dict(task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict[str, bool]:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()
        return {"ok": True}


@app.get("/report", response_model=ReportPublic)
def get_report() -> dict[str, object]:
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()

    status_count: dict[str, int] = {}
    owner_count: dict[str, int] = {}
    for task in tasks:
        status_count[task.status] = status_count.get(task.status, 0) + 1
        owner_count[task.owner] = owner_count.get(task.owner, 0) + 1

    return {
        "total": len(tasks),
        "status_count": status_count,
        "owner_count": owner_count,
    }
