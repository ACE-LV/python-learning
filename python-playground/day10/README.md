# Python 第十天：Pydantic 校验与响应模型

## 今日目标

把 FastAPI 的请求和响应写得更像前端熟悉的 DTO / interface。

你需要掌握：

1. 用 `BaseModel` 定义请求体。
2. 用 `Field` 约束字符串长度、数字范围。
3. 用 `Literal` 限定枚举值。
4. 用 `response_model` 控制接口返回结构。

## 学习顺序

1. 运行 `main.py`。
2. 打开 `/docs` 观察请求体 schema。
3. 尝试提交非法参数，看 FastAPI 如何返回 422。
4. 完成 `practice.py`。
5. 完成 `homework.py`。
6. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day10.main:app --reload
```

## 今日验收标准

- 能解释 422 和 404 的区别。
- 能用 `Field` 做基础字段约束。
- 能用 `response_model` 避免把内部字段直接返回给前端。
