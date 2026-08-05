# 第十二天学习总结模板

## 今天学了什么

- FastAPI 可以用 `Query` 接收前端表格传来的分页、搜索、筛选、排序参数。
- SQLAlchemy 查询通常先收集 `conditions`，再分别查 `total` 和当前页 `items`。
- `session.scalar(...)` 适合查一个值，比如总数；`session.scalars(...).all()` 适合查一组 ORM 对象。

## 一个前端表格接口通常需要哪些参数

- `page`：当前第几页。
- `page_size`：每页多少条。
- `keyword`：按名称搜索。
- `role` / `active`：筛选条件。
- `sort_by` / `sort_order`：排序字段和排序方向。

## 为什么返回 total 很重要

- `total` 是过滤之后、分页之前的总条数，前端分页器要靠它计算一共有多少页。
- 当前页的 `items` 只代表这一页的数据，`len(items)` 不能代表数据库里一共有多少条。
- 如果不返回 `total`，前端只能展示当前页，无法正确显示总数、总页数，也不知道还能不能继续翻页。

## 分页、筛选、排序的推荐顺序

1. 先根据 `keyword`、`role`、`active` 生成筛选条件。
2. 用相同条件查询 `total`。
3. 再按排序规则查询当前页，并加上 `offset` / `limit`。

## 今天完成的练习

- [x] 测试 page/page_size
- [x] 测试 keyword
- [x] 测试 role/active
- [x] 测试 sort_by/sort_order
- [x] 完成 homework

## 今天最容易混淆的点

- 排序不是筛选条件，不能把 `sort_by`、`sort_order` 放进 `conditions`。
- 分页返回值应该是一个对象，里面包含 `items` 和 `total`，不是只返回列表。
- `total` 要在 `offset` / `limit` 之前算。

## 明天想继续学什么

- 继续练习把接口拆成 `models`、`schemas`、`services` 多文件结构。
