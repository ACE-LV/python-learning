# Python 第四天：文件、JSON 与异常

## 今日目标

今天开始处理真实文件，这是写自动化脚本、数据处理工具、后端服务的基础。

你需要掌握：

1. 使用 `pathlib.Path` 处理路径。
2. 使用 `open()` / `Path.read_text()` 读取文本文件。
3. 使用 `json` 读取和写入 JSON。
4. 使用 `csv` 读取 CSV。
5. 使用 `try` / `except` 捕获常见错误。
6. 把文件处理逻辑封装成函数。

## 前端类比

| JavaScript / TypeScript | Python |
| --- | --- |
| Node.js `fs` | `pathlib` / `open()` |
| `JSON.parse()` | `json.loads()` / `json.load()` |
| `JSON.stringify()` | `json.dumps()` / `json.dump()` |
| `try { } catch { }` | `try:` / `except:` |
| `process.cwd()` | `Path.cwd()` |

## 今天重点

优先使用 `pathlib.Path`，少拼字符串路径：

```python
from pathlib import Path

file_path = Path("data/users.json")
text = file_path.read_text(encoding="utf-8")
```

读写文件时要明确编码：

```python
file_path.write_text("hello", encoding="utf-8")
```

## 学习顺序

1. 运行 `file_demo.py`。
2. 阅读 `js-vs-python.md`。
3. 完成 `practice.py`。
4. 完成 `homework.py`。
5. 写 `summary.md`。

## 今日验收标准

完成后你应该能：

- 知道 `Path` 比字符串路径更适合文件处理。
- 能读取 JSON 文件并转换成 Python 的 `list` / `dict`。
- 能把 Python 数据写回 JSON 文件。
- 能捕获文件不存在和 JSON 格式错误。
