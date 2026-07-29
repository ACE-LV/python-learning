# 第九天学习总结模板

## 今天学了什么

- 用 SQLAlchemy ORM 定义数据库表模型。
- 用 `engine` 连接数据库，用 `Session` 做查询、新增、更新、删除。
- 用 Pydantic `BaseModel` 定义 FastAPI 请求体，避免把 ORM 模型直接当请求体。

## ORM 是什么

- ORM 是 Object Relational Mapping，对象关系映射。
- 它把数据库表映射成 Python class，把表字段映射成对象属性。
- 使用 ORM 后，可以通过 `User(name="Ace", role="student")` 这种对象方式操作数据库，而不是每次手写 SQL。

## SQLAlchemy 三个关键对象

- `Model`：数据库表对应的 Python 类，例如 `User(Base)` 对应 `users` 表。
- `engine`：数据库入口，负责知道数据库在哪里、怎么连接。
- `Session`：一次数据库操作上下文，用来查询、添加、修改、删除 ORM 对象，并通过 `commit()` 提交。

## 今天完成的练习

- [x] 启动 day09 服务
- [x] 用 ORM 新增用户
- [x] 用 ORM 查询用户
- [x] 用 ORM 更新用户
- [x] 完成 homework

## 今天最容易混淆的点

- ORM 的 `User` 模型是数据库对象，不应该直接作为 FastAPI 请求体。
- FastAPI 请求体应该用 Pydantic `BaseModel`，例如 `UserCreate`、`UserUpdateRole`。
- `session.add()` 只是把对象加入会话，真正写入数据库要调用 `session.commit()`。
- `session.refresh()` 用来从数据库重新读取对象，比如拿到自动生成的 `id`。

## 明天想继续学什么

- 继续学习 SQLAlchemy 表关系，例如一对多、多对多。
