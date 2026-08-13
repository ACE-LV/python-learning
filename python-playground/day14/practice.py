# 第十四天练习题
# 主题：SQLAlchemy 多表关系

# 练习 1：新增 GET /users/{user_id}/courses。
# 要求：返回这个用户报名的所有课程。

# 练习 2：新增 DELETE /enrollments。
# 要求：请求体包含 user_id、course_id，删除报名关系。

# 练习 3：给 Course 新增 category 字段。
# 示例：backend、data、frontend。

# 练习 4：新增 GET /courses?level=beginner。
# 要求：按课程 level 过滤。

# 练习 5：思考：如果同一个用户重复报名同一门课，接口应该返回什么？

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, select
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "day14_practice.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

app = FastAPI(title="Day14 SQLAlchemy Relationships Homework")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    courses: Mapped[list["Course"]] = relationship(
        secondary="enrollments", back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 新增 category 字段
    students: Mapped[list[User]] = relationship(
        secondary="enrollments", back_populates="courses"
    )


enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


def init_db():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.scalar(select(User.id).limit(1)) is None:
            session.add_all(
                [
                    User(name="Alice", role="admin"),
                    User(name="Bob", role="user"),
                    User(name="Charlie", role="user"),
                ]
            )
            session.commit()

        if session.scalar(select(Course.id).limit(1)) is None:
            session.add_all(
                [
                    Course(title="Python Basics", level="beginner", category="backend"),
                    Course(title="Data Science 101", level="beginner", category="data"),
                    Course(
                        title="Frontend Development",
                        level="intermediate",
                        category="frontend",
                    ),
                ]
            )
            session.commit()

        alice = session.scalar(select(User).where(User.name == "Alice"))
        bob = session.scalar(select(User).where(User.name == "Bob"))
        python_course = session.scalar(
            select(Course).where(Course.title == "Python Basics")
        )
        data_course = session.scalar(
            select(Course).where(Course.title == "Data Science 101")
        )

        if python_course not in alice.courses:
            alice.courses.append(python_course)
        if data_course not in bob.courses:
            bob.courses.append(data_course)
        session.commit()


@app.on_event("startup")
def startup_event():
    init_db()


class EnrollmentRequest(BaseModel):
    user_id: int
    course_id: int


class UserCourseResponse(BaseModel):
    id: int
    title: str
    level: str
    category: str


class CourseResponse(BaseModel):
    id: int
    title: str
    level: str
    category: str


@app.get("/users/{user_id}/courses")
def get_user_courses(user_id: int) -> list[UserCourseResponse]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return [
            UserCourseResponse(
                id=course.id,
                title=course.title,
                level=course.level,
                category=course.category,
            )
            for course in user.courses
        ]


@app.delete("/enrollments")
def delete_enrollment(enrollment: EnrollmentRequest):
    with Session(engine) as session:
        user = session.get(User, enrollment.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        course = session.get(Course, enrollment.course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        if course in user.courses:
            user.courses.remove(course)
            session.commit()
            return {"message": "Enrollment deleted"}
        raise HTTPException(status_code=404, detail="Enrollment not found")


@app.get("/courses")
def get_courses(
    level: str | None = None, category: str | None = None
) -> list[CourseResponse]:
    with Session(engine) as session:
        query = select(Course)
        if level is not None:
            query = query.where(Course.level == level)
        if category is not None:
            query = query.where(Course.category == category)
        courses = session.scalars(query).all()
        return [
            CourseResponse(
                id=course.id,
                title=course.title,
                level=course.level,
                category=course.category,
            )
            for course in courses
        ]

