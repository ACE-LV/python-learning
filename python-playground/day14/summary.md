# 第十四天学习总结模板

## 今天学了什么

- 用 SQLAlchemy 建立 `users`、`courses` 和 `enrollments` 三张表。
- 用 `relationship(..., secondary=...)` 表达用户和课程的多对多关系。
- 用 `user.courses.append(course)` 创建报名关系。

## 一对多和多对多的区别

- 一对多：一条 A 数据可以关联多条 B 数据，但一条 B 数据通常只属于一条 A 数据，比如一个作者有多篇文章。
- 多对多：一条 A 数据可以关联多条 B 数据，一条 B 数据也可以关联多条 A 数据，比如一个用户可以报名多门课程，一门课程也可以有多个用户报名。

## 为什么需要 enrollments 中间表

- 因为用户和课程是多对多关系，单独在 `users` 表或 `courses` 表里放一个外键都不够。
- 如果在 `users` 表里只放 `course_id`，一个用户只能表示报名一门课。
- 如果在 `courses` 表里只放 `user_id`，一门课只能表示一个学生。
- 所以需要 `enrollments` 中间表，用 `user_id + course_id` 表示一条报名关系。
- `user_id` 指向用户，`course_id` 指向课程，同一个用户可以有多条报名记录，同一门课程也可以被多个用户报名。

## 今天完成的练习

- [x] 启动 day14 服务
- [x] 调用 seed 接口
- [x] 查询用户课程
- [x] 查询课程学员
- [x] 完成 homework

## 今天最容易混淆的点

- `User` / `Course` 是 ORM 模型，负责数据库表；`UserCreate` / `CourseCreate` 是 Pydantic 模型，负责接口请求体。
- `course.students` 里每一项是 `User` 对象，所以返回学生姓名时要取 `student.name`。
- `create_all()` 只会创建不存在的表，不会自动迁移已经存在的表结构。

## 明天想继续学什么

- 学习数据库迁移，理解表结构变化后怎么安全升级数据库。
