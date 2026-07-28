# Python 第十六天：FastAPI 接口测试

## 今日目标

用 `pytest` 和 `TestClient` 给 FastAPI 接口写自动化测试。

你需要掌握：

1. 用 `TestClient` 模拟 HTTP 请求。
2. 断言状态码和响应 JSON。
3. 用 fixture 重置测试数据。
4. 测试成功场景和失败场景。

## 学习顺序

1. 安装依赖：`pytest`、`httpx`。
2. 阅读 `main.py`。
3. 阅读 `test_main.py`。
4. 运行测试。
5. 完成 `practice.py`。
6. 完成 `homework.py`。
7. 更新 `summary.md`。

## 安装依赖

```powershell
python -m pip install pytest httpx
```

## 运行测试

```powershell
python -m pytest .\python-playground\day16\ -q
```

## 今日验收标准

- 能写接口成功测试。
- 能写 404、422 失败测试。
- 能理解自动化测试比手点 `/docs` 更适合回归。
