# Python 第十四天：SQLAlchemy 关系表

## 今日目标

从单表用户接口升级到多表关系：用户、课程、报名关系。

你需要掌握：

1. 一对多和多对多的基本概念。
2. 用中间表表达 `users <-> courses`。
3. 用 SQLAlchemy `relationship` 读取关联数据。
4. 用接口完成报名和查询课程学员。

## 学习顺序

1. 安装依赖：`sqlalchemy`。
2. 运行 `main.py`。
3. 先调用 `POST /seed` 生成演示数据。
4. 测试课程、用户、报名接口。
5. 完成 `practice.py`。
6. 完成 `homework.py`。
7. 运行 `pandas_demo.py`，用表格方式查看报名数据。
8. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day14.main:app --reload
```

## 今日验收标准

- 能解释为什么多对多需要中间表。
- 能查询某门课程有哪些学生。
- 能查询某个用户报名了哪些课程。
- 能用 pandas 把用户、课程、报名三张表合并成一张可读报表。

## 今日 pandas 加餐

pandas 可以把数据库、CSV、Excel、接口数据变成类似前端表格/Excel 的 `DataFrame`，方便筛选、排序、分组统计和导出报表。

运行示例：

```powershell
python .\python-playground\day14\pandas_demo.py
```

今天先学 3 个动作：

1. `read_sql_query()`：从 SQLite 读取表数据。
2. `merge()`：像 SQL join 一样合并用户、课程、报名表。
3. `groupby()`：按课程统计报名人数。
