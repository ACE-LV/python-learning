from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# 第 18 天主题：综合项目。
# 把 FastAPI、Pydantic、SQLAlchemy ORM、筛选查询、CRUD、统计报表串起来。

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day18_tasks.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

# SQLite engine。这里是真实文件数据库，不再只是内存 list。
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
app = FastAPI(title="Day18 Learning Task Tracker")

# 任务状态枚举。
# 用 Literal 可以让 status 只能是 todo/doing/done，非法值会自动返回 422。
TaskStatus = Literal["todo", "doing", "done"]


class Base(DeclarativeBase):
    # ORM 模型基类。Task 继承它后，SQLAlchemy 会把 Task 注册到 Base.metadata。
    pass


class Task(Base):
    # 数据库模型：对应 tasks 表。
    # 注意：这是 ORM 模型，不是 API 请求体，也不直接暴露给前端。
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # title 是任务标题，数据库字段最多 120 字符。
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    # status 默认 todo，表示新任务还没开始。
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)
    # priority 越小优先级越高；列表查询里会按 priority 排序。
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    # owner 表示负责人。
    owner: Mapped[str] = mapped_column(String(50), nullable=False)


class TaskCreate(BaseModel):
    # 创建任务请求体。
    # 这是前端 POST /tasks 时需要提交的数据。
    title: str = Field(min_length=1, max_length=120)
    owner: str = Field(min_length=1, max_length=50)
    # priority 默认 3，合法范围 1-5。
    priority: int = Field(default=3, ge=1, le=5)


class TaskUpdateStatus(BaseModel):
    # 更新任务状态请求体。
    # 单独定义这个模型，是为了这个接口只能改 status，不能顺手改 title/owner。
    status: TaskStatus


class TaskPublic(BaseModel):
    # 返回给前端的任务结构。
    # response_model=TaskPublic 会控制输出字段，避免把 ORM 内部状态返回出去。
    id: int
    title: str
    status: TaskStatus
    priority: int
    owner: str


class ReportPublic(BaseModel):
    # /report 的响应结构。
    # 报表不是单个任务，所以单独建响应模型。
    total: int
    # 按状态统计任务数量，例如 {"todo": 3, "done": 2}。
    status_count: dict[str, int]
    # 按负责人统计任务数量，例如 {"Ace": 2, "Bob": 1}。
    owner_count: dict[str, int]


def init_db() -> None:
    # 根据 Task 模型创建 tasks 表。
    Base.metadata.create_all(bind=engine)


def task_to_dict(task: Task) -> dict[str, object]:
    # ORM 对象转 API dict。
    # 不直接返回 task.__dict__，因为 SQLAlchemy 对象里有内部状态字段。
    return {
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "priority": task.priority,
        "owner": task.owner,
    }


@app.on_event("startup")
def on_startup() -> None:
    # 服务启动时确保数据库表存在。
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口。
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskPublic)
def create_task(payload: TaskCreate) -> dict[str, object]:
    # 创建任务：Pydantic 先校验 payload，再进入函数体。
    with Session(engine) as session:
        task = Task(title=payload.title, owner=payload.owner, priority=payload.priority)
        session.add(task)
        # commit 真正写入数据库。
        session.commit()
        # refresh 读取数据库生成的 id/default status 回 Python 对象。
        session.refresh(task)
        return task_to_dict(task)


@app.get("/tasks", response_model=list[TaskPublic])
def list_tasks(
    # 可选筛选条件：不传就是不过滤。
    status: TaskStatus | None = Query(default=None),
    owner: str | None = Query(default=None),
) -> list[dict[str, object]]:
    # select(Task) 表示查询 Task 表对应的 ORM 对象。
    # order_by(Task.priority, Task.id) 让列表稳定排序：先按优先级，再按 id。
    stmt = select(Task).order_by(Task.priority, Task.id)
    if status is not None:
        # where 条件会被 SQLAlchemy 转成 SQL WHERE。
        stmt = stmt.where(Task.status == status)
    if owner is not None:
        stmt = stmt.where(Task.owner == owner)

    with Session(engine) as session:
        # scalars(select(Task)) 返回 Task 对象列表，而不是 Row tuple。
        tasks = session.scalars(stmt).all()
        return [task_to_dict(task) for task in tasks]


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(task_id: int) -> dict[str, object]:
    with Session(engine) as session:
        # session.get(Task, task_id) 按主键查询单条任务。
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

    # 修改 ORM 对象属性，commit 时 SQLAlchemy 会生成 UPDATE。
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

    # delete 标记对象为删除，commit 后数据库记录才真正被删除。
        session.delete(task)
        session.commit()
        return {"ok": True}


@app.get("/report", response_model=ReportPublic)
def get_report() -> dict[str, object]:
    # 报表接口：先查询所有任务，再在 Python 中统计。
    # 数据量大时可以改成 SQL GROUP BY；学习阶段先用 Python 字典计数更直观。
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()

    status_count: dict[str, int] = {}
    owner_count: dict[str, int] = {}
    for task in tasks:
        # dict.get(key, 0) 表示没有这个 key 时从 0 开始计数。
        status_count[task.status] = status_count.get(task.status, 0) + 1
        owner_count[task.owner] = owner_count.get(task.owner, 0) + 1

    return {
        "total": len(tasks),
        "status_count": status_count,
        "owner_count": owner_count,
    }
