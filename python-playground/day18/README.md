# Python 第十八天：综合项目 - 学习任务追踪 API

## 今日目标

把前面学过的 FastAPI、Pydantic、SQLAlchemy、分页思路和报表组合成一个小项目。

项目主题：学习任务追踪 API。

你需要掌握：

1. 用数据库保存任务。
2. 新增、查询、更新状态、删除任务。
3. 按状态和负责人筛选。
4. 输出任务统计报表。

## 学习顺序

1. 安装依赖：`fastapi`、`uvicorn`、`sqlalchemy`。
2. 运行 `main.py`。
3. 打开 `/docs` 创建几条任务。
4. 测试筛选、状态更新、报表。
5. 完成 `practice.py`。
6. 完成 `homework.py`。
7. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day18.main:app --reload
```

## 今日验收标准

- 能完整跑通任务 CRUD。
- 能解释请求模型和数据库模型的区别。
- 能把这个项目讲成一个简历里的 Python 入门项目。
