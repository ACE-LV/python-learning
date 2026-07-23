# Python 第七天：测试、日志与工程化

## 今日目标

今天你会把“能跑”进阶到“可维护”：

1. 用 `pytest` 写基础单元测试。
2. 用 `logging` 打印结构化日志。
3. 理解基础工程化工具：`black`、`ruff`、`isort`。

## 学习顺序

1. 运行 `logging_demo.py`。
2. 阅读 `js-vs-python.md`。
3. 完成 `calculator.py` + `test_calculator.py`。
4. 运行 pytest。
5. 完成 `homework.py` 和 `summary.md`。

## 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
```

## 跑测试

```powershell
.\.venv\Scripts\python.exe -m pytest .\python-playground\day07\ -q
```

## 今日验收标准

- 能写最基础的 3-5 个测试用例。
- 知道日志分级（INFO/WARNING/ERROR）。
- 能理解“先写断言再实现逻辑”的思路。
