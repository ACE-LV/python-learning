# Python 第十二天：分页、搜索与排序

## 今日目标

实现前端表格页最常见的接口能力：分页、搜索、筛选、排序。

你需要掌握：

1. Query 参数的默认值和范围校验。
2. 返回 `items + total + page + page_size`。
3. 搜索关键词 `keyword`。
4. 按字段排序 `sort_by` / `sort_order`。

## 学习顺序

1. 运行 `main.py`。
2. 打开 `/docs` 测试 `/users` 的 query 参数。
3. 分别测试分页、角色筛选、关键词搜索、排序。
4. 完成 `practice.py`。
5. 完成 `homework.py`。
6. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day12.main:app --reload
```

## 示例请求

```text
GET /users?page=1&page_size=5&keyword=a&role=frontend&sort_by=name&sort_order=asc
```

## 今日验收标准

- 能设计适合前端表格的分页响应。
- 能理解分页应该在过滤和排序之后做。
- 能解释 `total` 为什么不能只返回当前页数量。
