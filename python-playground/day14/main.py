from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day14_courses.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
app = FastAPI(title="Day14 SQLAlchemy Relationships")


class Base(DeclarativeBase):
    pass


enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    courses: Mapped[list[Course]] = relationship(secondary=enrollments, back_populates="students")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    students: Mapped[list[User]] = relationship(secondary=enrollments, back_populates="courses")


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    role: str = Field(min_length=1, max_length=50)


class CourseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    level: str = Field(min_length=1, max_length=20)


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
        "course_ids": [course.id for course in user.courses],
    }


def course_to_dict(course: Course) -> dict[str, object]:
    return {
        "id": course.id,
        "title": course.title,
        "level": course.level,
        "student_ids": [student.id for student in course.students],
    }


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.post("/seed")
def seed_data() -> dict[str, int | str]:
    with Session(engine) as session:
        existing_user = session.scalar(select(User).limit(1))
        if existing_user is not None:
            return {"message": "already seeded", "users": 0, "courses": 0}

        alice = User(name="Alice", role="frontend")
        bob = User(name="Bob", role="backend")
        python_course = Course(title="Python API", level="beginner")
        sql_course = Course(title="SQL for Backend", level="beginner")
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
        user = session.get(User, payload.user_id)
        course = session.get(Course, payload.course_id)
        if user is None or course is None:
            raise HTTPException(status_code=404, detail="User or course not found")

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
        return [user_to_dict(student) for student in course.students]
