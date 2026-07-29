from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

# 第 14 天主题：SQLAlchemy 表关系。
# 场景：用户可以报名多门课程，一门课程也可以有多个用户报名，这是典型“多对多”。

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day14_courses.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

# engine 是数据库入口；这里继续用 SQLite 文件数据库。
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
app = FastAPI(title="Day14 SQLAlchemy Relationships")


class Base(DeclarativeBase):
    # 所有 ORM 模型的基类。
    # User/Course 继承 Base 后，SQLAlchemy 才能收集表结构到 Base.metadata。
    pass


enrollments = Table(
    # 中间表：专门保存“谁报名了哪门课”。
    # 为什么多对多需要中间表：
    # - users 表一行只能表示一个用户。
    # - courses 表一行只能表示一门课。
    # - 一个用户和一门课之间的报名关系可能有很多条，只能用第三张表记录。
    "enrollments",
    Base.metadata,
    # user_id 指向 users.id。
    # primary_key=True 表示同一个 user_id + course_id 组合不能重复。
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    # course_id 指向 courses.id。
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    # courses 是 ORM 关系属性，不是 users 表里的真实字段。
    # secondary=enrollments 表示通过 enrollments 中间表找到课程。
    # back_populates="students" 表示它和 Course.students 是一组双向关系。
    # 用法：user.courses.append(course) 就是在 enrollments 里新增一条报名关系。
    courses: Mapped[list[Course]] = relationship(secondary=enrollments, back_populates="students")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    # students 也是 ORM 关系属性，不是 courses 表里的真实字段。
    # 它通过同一张 enrollments 中间表反查报名这门课的用户。
    # 用法：course.students 可以拿到报名这门课的 User 列表。
    students: Mapped[list[User]] = relationship(secondary=enrollments, back_populates="courses")


class UserCreate(BaseModel):
    # 创建用户接口的请求体。
    name: str = Field(min_length=1, max_length=50)
    role: str = Field(min_length=1, max_length=50)


class CourseCreate(BaseModel):
    # 创建课程接口的请求体。
    title: str = Field(min_length=1, max_length=100)
    level: str = Field(min_length=1, max_length=20)


class EnrollmentCreate(BaseModel):
    # 报名接口请求体。
    # 它不创建用户/课程，只创建 user 和 course 之间的关系。
    user_id: int
    course_id: int


def init_db() -> None:
    # 根据 Base.metadata 中收集到的 User、Course、enrollments 创建表。
    Base.metadata.create_all(bind=engine)


def user_to_dict(user: User) -> dict[str, object]:
    # 把 ORM User 对象转成 API 可返回的 dict。
    # course_ids 来自关系属性 user.courses，不是 users 表里的普通列。
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "course_ids": [course.id for course in user.courses],
    }


def course_to_dict(course: Course) -> dict[str, object]:
    # 把 ORM Course 对象转成 API 可返回的 dict。
    # student_ids 来自关系属性 course.students。
    return {
        "id": course.id,
        "title": course.title,
        "level": course.level,
        "student_ids": [student.id for student in course.students],
    }


@app.on_event("startup")
def on_startup() -> None:
    # 服务启动时确保表存在。
    init_db()


@app.post("/seed")
def seed_data() -> dict[str, int | str]:
    # 生成演示数据，方便打开 /docs 后快速测试关系接口。
    with Session(engine) as session:
        existing_user = session.scalar(select(User).limit(1))
        if existing_user is not None:
            return {"message": "already seeded", "users": 0, "courses": 0}

        alice = User(name="Alice", role="frontend")
        bob = User(name="Bob", role="backend")
        python_course = Course(title="Python API", level="beginner")
        sql_course = Course(title="SQL for Backend", level="beginner")
        # 通过关系属性新增报名关系。
        # SQLAlchemy 会在 commit 时自动往 enrollments 中间表插入对应 user_id/course_id。
        alice.courses.append(python_course)
        bob.courses.extend([python_course, sql_course])
        session.add_all([alice, bob, python_course, sql_course])
        session.commit()
        return {"message": "seeded", "users": 2, "courses": 2}


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    with Session(engine) as session:
        user = User(name=payload.name, role=payload.role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user_to_dict(user)


@app.post("/courses")
def create_course(payload: CourseCreate) -> dict[str, object]:
    with Session(engine) as session:
        course = Course(title=payload.title, level=payload.level)
        session.add(course)
        session.commit()
        session.refresh(course)
        return course_to_dict(course)


@app.post("/enrollments")
def enroll_user(payload: EnrollmentCreate) -> dict[str, object]:
    with Session(engine) as session:
        # 先分别确认用户和课程存在。
        user = session.get(User, payload.user_id)
        course = session.get(Course, payload.course_id)
        if user is None or course is None:
            raise HTTPException(status_code=404, detail="User or course not found")

        # 避免重复报名。
        # 如果 course 已经在 user.courses 里，就不重复 append。
        if course not in user.courses:
            user.courses.append(course)
        session.commit()
        session.refresh(user)
        return user_to_dict(user)


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user_to_dict(user)


@app.get("/courses/{course_id}")
def get_course(course_id: int) -> dict[str, object]:
    with Session(engine) as session:
        course = session.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course_to_dict(course)


@app.get("/courses/{course_id}/students")
def list_course_students(course_id: int) -> list[dict[str, object]]:
    with Session(engine) as session:
        course = session.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        # course.students 是通过 enrollments 中间表查出来的报名用户列表。
        return [user_to_dict(student) for student in course.students]
