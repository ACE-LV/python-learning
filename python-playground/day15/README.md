# Python 第十五天：数据库迁移入门

## 今日目标

理解“表结构变化”不能靠手动改库，需要可追踪的 migration。

你需要掌握：

1. migration 是什么。
2. 为什么不能随便删表重建。
3. 如何记录当前数据库版本。
4. 如何用脚本安全地给表加字段。

## 学习顺序

1. 运行 `migration_demo.py`。
2. 观察第一次运行创建了哪些表。
3. 再运行一次，观察 migration 不会重复执行。
4. 打开生成的 `day15_migration.db`。
5. 完成 `practice.py`。
6. 完成 `homework.py`。
7. 更新 `summary.md`。

## 运行脚本

```powershell
python .\python-playground\day15\migration_demo.py
```

## 今日验收标准

- 能解释 migration 和普通 SQL 脚本的区别。
- 能理解版本表 `schema_migrations` 的作用。
- 能写一个“只执行一次”的表结构变更。
