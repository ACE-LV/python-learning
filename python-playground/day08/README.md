# Python 第八天：FastAPI + SQLite 持久化

## 今日目标

把前几天“内存列表 API”升级为“真实数据库 API”。

你需要掌握：

1. 使用 `sqlite3` 初始化数据表。
2. 在 FastAPI 路由中读写 SQLite。
3. 通过 `GET/POST/PATCH` 实现基础 CRUD。
4. 继续使用 `Pydantic BaseModel` 做请求体校验。

## 学习顺序

1. 运行 `main.py`，自动初始化数据库。
2. 打开 `/docs` 测试接口。
3. 阅读 `practice.py` 并补全练习。
4. 完成 `homework.py`。
5. 更新 `summary.md`。

## 启动服务

```powershell
.\.venv\Scripts\python.exe -m uvicorn python-playground.day08.main:app --reload
```

## 文档地址

```text
http://127.0.0.1:8000/docs
```

## 今日验收标准

- 能成功新增并查询数据库里的用户。
- 能完成角色更新接口。
- 能输出 report（总数、active 数、角色统计）。
