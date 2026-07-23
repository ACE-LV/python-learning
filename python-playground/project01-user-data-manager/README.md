# Project 01: User Data Manager (SQLite)

一个面向练手的 Python 小项目：

- 使用 `sqlite3` 对接数据库
- 支持用户数据的增、查、停用
- 支持从 JSON 批量导入
- 生成简单报表

## 目录

- `src/main.py`：项目主程序（CLI）
- `data/users_seed.json`：种子数据
- `data/users.db`：SQLite 数据库文件（运行后生成）

## 快速开始

在 `python-learning` 目录运行：

```powershell
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py init-db
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py seed
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py list
.\.venv\Scripts\python.exe .\python-playground\project01-user-data-manager\src\main.py report
```

## 命令说明

- `init-db`：初始化数据库表
- `seed`：从 `data/users_seed.json` 导入用户
- `list`：列出全部用户
- `add --name Ace --role frontend`：新增用户
- `deactivate --user-id 1`：停用用户
- `report`：输出统计报表

## 练手建议

1. 给 `add` 增加参数校验（空字符串、非法 role）。
2. 给 `list` 增加筛选参数（只看 active/frontend）。
3. 给 `report` 增加导出 JSON 文件能力。
4. 再加一个 `delete --user-id` 命令。
