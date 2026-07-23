# Python 第六天：FastAPI 入门（直接实战）

## 今日目标

今天直接上 FastAPI，完成一个最小可运行 API 服务。

你需要掌握：

1. 创建 FastAPI 应用。
2. 定义 `GET` / `POST` 路由。
3. 使用 Pydantic 模型做请求体校验。
4. 启动服务并在 Swagger 页面测试接口。

## 学习顺序

1. 安装依赖：`fastapi`、`uvicorn`。
2. 运行 `main.py`。
3. 打开 `http://127.0.0.1:8000/docs` 测接口。
4. 完成 `practice.py`。
5. 完成 `homework.py`。

## 安装依赖

在 `python-learning` 目录运行：

```powershell
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn
```

## 启动方式

```powershell
.\.venv\Scripts\python.exe -m uvicorn python-playground.day06.main:app --reload
```

如果你在 `day06` 目录运行，也可以：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## 今日验收标准

完成后你应该能：

- 启动 FastAPI 服务并访问 `/docs`。
- 理解请求参数、请求体、响应结构。
- 独立新增一个简单接口。
