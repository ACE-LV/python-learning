# Python Learning

这是 Python 学习专用目录，学习文件和虚拟环境都放在这里。

## 目录结构

- `.venv`：当前正在使用的 Python 虚拟环境。
- `python-playground`：每天的练习代码。
- `python-learning-course-for-frontend.md`：完整 8 周学习路线。
- `data`：本地 SQLite 学习数据库。
- `sql`：SQL 初始化脚本和查询练习。

## VS Code 解释器选择

请选择这个解释器：

```powershell
c:\Users\ace.lv\workspace\project\python-learning\.venv\Scripts\python.exe
```

## 每次学习前先进入目录

```powershell
Set-Location "c:\Users\ace.lv\workspace\project\python-learning"
```

## 查看 Python 版本

```powershell
.\.venv\Scripts\python.exe --version
```

## 运行第一天示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day01\hello.py
```

## 运行第一天练习

```powershell
.\.venv\Scripts\python.exe .\python-playground\day01\practice.py
```

## 运行第一天作业

```powershell
.\.venv\Scripts\python.exe .\python-playground\day01\homework.py
```

## 运行第二天示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day02\collections_demo.py
```

## 运行第二天练习

```powershell
.\.venv\Scripts\python.exe .\python-playground\day02\practice.py
```

## 运行第二天作业

```powershell
.\.venv\Scripts\python.exe .\python-playground\day02\homework.py
```

## 运行第三天示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day03\functions_demo.py
```

## 运行第三天模块示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day03\module_demo.py
```

## 运行第三天练习

```powershell
.\.venv\Scripts\python.exe .\python-playground\day03\practice.py
```

## 运行第三天作业

```powershell
.\.venv\Scripts\python.exe .\python-playground\day03\homework.py
```

## 运行第四天示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day04\file_demo.py
```

## 运行第四天练习

```powershell
.\.venv\Scripts\python.exe .\python-playground\day04\practice.py
```

## 运行第四天作业

```powershell
.\.venv\Scripts\python.exe .\python-playground\day04\homework.py
```

## 运行第五天示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day05\class_demo.py
```

## 运行第五天练习

```powershell
.\.venv\Scripts\python.exe .\python-playground\day05\practice.py
```

## 运行第五天作业

```powershell
.\.venv\Scripts\python.exe .\python-playground\day05\homework.py
```

## 安装第六天依赖

```powershell
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn
```

## 运行第六天示例（FastAPI）

```powershell
.\.venv\Scripts\python.exe -m uvicorn python-playground.day06.main:app --reload
```

## 打开接口文档

```text
http://127.0.0.1:8000/docs
```

## 安装第七天依赖

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
```

## 运行第七天日志示例

```powershell
.\.venv\Scripts\python.exe .\python-playground\day07\logging_demo.py
```

## 运行第七天测试

```powershell
.\.venv\Scripts\python.exe -m pytest .\python-playground\day07\ -q
```

## SQLTools 配置

当前工作区已经配置了 SQLTools SQLite 连接：

```text
Python Learning SQLite
```

数据库文件：

```text
c:\Users\ace.lv\workspace\project\python-learning\data\learning.db
```

### 重新生成学习数据库

```powershell
Set-Location "c:\Users\ace.lv\workspace\project\python-learning"
.\.venv\Scripts\python.exe .\sql\init_learning_db.py
```

### 在 SQLTools 中连接数据库

1. 点击 VS Code 左侧 SQLTools 图标。
2. 找到连接 `Python Learning SQLite`。
3. 点击连接按钮。
4. 打开 `sql/day01-basic-queries.sql`。
5. 选中一条 SQL。
6. 点击右上角 `Run on active connection`，或右键选择执行查询。

### 第一批练习 SQL

```sql
SELECT * FROM users;
SELECT * FROM courses;
SELECT * FROM users WHERE role = 'Frontend Developer';
```

## 推荐学习顺序

1. 打开当天目录里的 `README.md`。
2. 运行当天示例文件。
3. 修改并运行当天 `practice.py`。
4. 独立完成当天 `homework.py`。
5. 在当天 `summary.md` 写学习总结。
