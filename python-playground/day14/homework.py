# 第十四天作业
# 主题：用户、课程、报名关系 API

# 作业要求：
# 1. 建立 users 表。
# 2. 建立 courses 表。
# 3. 建立 enrollments 中间表。
# 4. 完成创建用户、创建课程。
# 5. 完成用户报名课程。
# 6. 完成查询课程学员。
# 7. 完成查询用户课程。
# 8. 在 summary.md 写清楚多对多为什么需要中间表。

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day14_homework.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

app = FastAPI(title="Day14 SQLAlchemy Relationships Homework")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


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
    courses: Mapped[list["Course"]] = relationship(
        secondary=enrollments, back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    students: Mapped[list[User]] = relationship(
        secondary=enrollments, back_populates="courses"
    )


class UserCreate(BaseModel):
    name: str


class CourseCreate(BaseModel):
    title: str


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class UserResponse(BaseModel):
    id: int
    name: str
    courses: list[str]


class CourseResponse(BaseModel):
    id: int
    title: str
    students: list[str]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.scalar(select(User.id).limit(1)) is None:
            session.add_all(
                [
                    User(name="Alice"),
                    User(name="Bob"),
                    User(name="Charlie"),
                ]
            )
            session.commit()

        if session.scalar(select(Course.id).limit(1)) is None:
            session.add_all(
                [
                    Course(title="Python Basics"),
                    Course(title="Data Science 101"),
                ]
            )
            session.commit()


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.post("/users")
def create_user(payload: UserCreate) -> UserResponse:
    with Session(engine) as session:
        existing_user = session.scalar(select(User).where(User.name == payload.name))
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(name=payload.name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {
            "id": user.id,
            "name": user.name,
            "courses": [course.title for course in user.courses],
        }


@app.post("/courses")
def create_course(payload: CourseCreate) -> CourseResponse:
    with Session(engine) as session:
        existing_course = session.scalar(
            select(Course).where(Course.title == payload.title)
        )
        if existing_course is not None:
            raise HTTPException(status_code=400, detail="Course already exists")

        course = Course(title=payload.title)
        session.add(course)
        session.commit()
        session.refresh(course)
        return {
            "id": course.id,
            "title": course.title,
            "students": [student.name for student in course.students],
        }


@app.post("/enrollments")
def enroll_user(payload: EnrollmentCreate) -> UserResponse:
    with Session(engine) as session:
        user = session.get(User, payload.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        course = session.get(Course, payload.course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")

        if course not in user.courses:
            user.courses.append(course)
            session.commit()
            session.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "courses": [course.title for course in user.courses],
        }


@app.get("/courses/{course_id}/students")
def get_course_students(course_id: int) -> CourseResponse:
    with Session(engine) as session:
        course = session.get(Course, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return {
            "id": course.id,
            "title": course.title,
            "students": [student.name for student in course.students],
        }


@app.get("/users/{user_id}/courses")
def get_user_courses(user_id: int) -> UserResponse:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": user.id,
            "name": user.name,
            "courses": [course.title for course in user.courses],
        }
