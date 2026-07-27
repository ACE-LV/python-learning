# Python 第九天：SQLAlchemy ORM 入门

## 今日目标

把 day08 的 `sqlite3` 手写 SQL 改成 SQLAlchemy ORM 写法。

你需要掌握：

1. 用 `User` 类映射数据库表。
2. 用 `Session` 查询、新增、更新数据。
3. 理解 ORM 和前端状态对象的相似点与差异。
4. 保留 FastAPI 的 `GET/POST/PATCH` 接口形式。

## 学习顺序

1. 安装依赖：`sqlalchemy`。
2. 运行 `main.py`。
3. 打开 `/docs` 测试用户接口。
4. 阅读 `practice.py` 并补全练习。
5. 完成 `homework.py`。
6. 更新 `summary.md`。

## 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install sqlalchemy
```

## 启动服务

```powershell
.\.venv\Scripts\python.exe -m uvicorn python-playground.day09.main:app --reload
```

## 今日验收标准

- 能说出 `Model`、`engine`、`Session` 分别做什么。
- 能用 ORM 完成新增、查询、更新。
- 能理解 `session.commit()` 和 `session.refresh()` 的作用。
