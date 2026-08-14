# 第十五天学习总结模板

## 今天学了什么

- migration 用版本化脚本记录数据库结构变化。
- `schema_migrations` 用来判断某个版本是否已经执行。
- 表结构变更成功后，才把对应版本写入迁移记录表。

## migration 是什么

- migration 是数据库结构的变更记录，例如创建表、增加字段和创建索引。
- 它让开发、测试和生产环境可以按相同顺序升级数据库，而不是手动改表。

## 为什么要记录 schema_migrations

- 避免重复执行 `ALTER TABLE ADD COLUMN`，否则会出现字段重复错误。
- 可以知道当前数据库已经升级到哪个版本，方便部署、排查和审计。
- 迁移的风险是错误 SQL 可能导致数据丢失、锁表或服务不可用，因此生产执行前要备份、评审并准备回滚方案。

## 今天完成的练习

- [x] 第一次运行 migration_demo.py
- [x] 第二次运行 migration_demo.py
- [x] 查看 users 表字段
- [x] 查看 schema_migrations
- [x] 完成 homework

## 今天最容易混淆的点

- `IF NOT EXISTS` 只能保护建表；`ALTER TABLE ADD COLUMN` 仍然要靠迁移版本避免重复执行。
- migration SQL 和 migration 版本记录要在同一个事务中成功提交。

## 明天想继续学什么

- 学习 Alembic 如何自动生成和执行真实项目的 migration。
