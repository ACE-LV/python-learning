# 第十天学习总结模板

## 今天学了什么

- 用 Pydantic `BaseModel` 定义请求和响应模型。
- 用 `Field` 对字符串长度和数字范围做运行时校验。
- 用 `response_model` 约束接口返回结构，避免返回多余内部字段。

## Pydantic 和 TypeScript interface 的区别

- TypeScript interface 主要是编译期类型提示，运行时不会自动校验请求数据。
- Pydantic `BaseModel` 会在运行时校验请求体，校验失败直接由 FastAPI 返回 422。

## 422 和 404 的区别

- `422`：请求参数/请求体格式不符合规则，例如 `name=""` 或 `age=999`。
- `404`：请求格式正确，但目标资源不存在，例如 `GET /users/999` 找不到用户。

## 今天完成的练习

- [x] 启动 day10 服务
- [x] 测试合法请求
- [x] 测试非法请求
- [x] 完成 response_model
- [x] 完成 homework

## 今天最容易混淆的点

- `Query(default=None)` 和 `= None` 在简单场景效果接近，但 `Query` 更适合加约束和文档说明。
- `payload.dict(exclude_none=True)` 用在 PATCH 时只更新前端传入的字段。

## 明天想继续学什么

- 学习如何把一个接口拆成 `main.py`、`schemas.py`、`services.py` 的分层结构。
