# Python 第十三天：依赖注入与简单鉴权

## 今日目标

理解 FastAPI 的 `Depends`，并实现一个最小可运行的 token 鉴权。

你需要掌握：

1. 用依赖函数复用公共逻辑。
2. 从请求头读取 `Authorization`。
3. 对受保护接口返回 401。
4. 区分公开接口和需要登录的接口。

## 学习顺序

1. 运行 `main.py`。
2. 打开 `/docs`。
3. 先直接访问受保护接口，观察 401。
4. 在请求头加入 `Authorization: Bearer dev-token`。
5. 完成 `practice.py`。
6. 完成 `homework.py`。
7. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day13.main:app --reload
```

## 测试请求头

```text
Authorization: Bearer dev-token
```

## 今日验收标准

- 能解释 `Depends(require_token)` 的执行时机。
- 能让公开接口无需 token。
- 能让受保护接口缺 token 时返回 401。
