# Day12 额外练习：数据库查询手感训练

目标：把 `select`、`where`、`scalars`、`scalar`、`count`、`order_by`、`offset`、`limit` 练到有画面。

建议做法：每次只做一道题，写完就用 `/docs` 或 `TestClient` 验证，不要一次性全写完。

## 练习 0：先确认基础数据

先打开 `practice.py`，确认 seed 数据里至少有：

```text
Alice   active=True
Bob     active=True
Cindy   active=False
Daniel  active=True
Eva     active=False
```

然后启动服务，访问：

```text
GET /users/simple
```

你应该看到所有用户。

## 练习 1：只查 active=true

新增一个接口：

```text
GET /users/active-only
```

要求：

- 使用真实数据库查询。
- 使用 `Session(engine)`。
- 使用 `select(User).where(User.active == True)`。
- 使用 `session.scalars(...).all()`。

目标脑图：

```text
select(User).where(...)
        ↓
session.scalars(...).all()
        ↓
[User(...), User(...)]
```

预期结果：只返回 Alice、Bob、Daniel。

## 练习 2：只查 inactive 用户

新增接口：

```text
GET /users/inactive-only
```

要求：

- 条件是 `User.active == False`。
- 返回 Cindy、Eva。

思考：为什么这里用 `== False` 比 `is False` 更适合数据库查询？

## 练习 3：按 name 搜索

给 `/users` 增加一个可选参数：

```python
keyword: str | None = Query(None)
```

要求：

- 如果 `keyword` 有值，就加条件：

```python
func.lower(User.name).contains(keyword.lower())
```

请求示例：

```text
GET /users?keyword=an
```

预期：能匹配 Daniel、Frank（如果你的 seed 里有 Frank）。

目标脑图：

```text
前端 params.keyword
        ↓
FastAPI Query
        ↓
where lower(name) contains keyword
```

## 练习 4：返回分页对象，而不是只返回列表

当前 `practice.py` 的 `/users` 返回的是：

```python
list[UserResponse]
```

请改成返回：

```json
{
  "items": [],
  "total": 5,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

要求新增 Pydantic 模型：

```python
class PageResult(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
```

重点：

- `items` 是当前页数据。
- `total` 是过滤后的总数。
- `total` 不能用 `len(items)` 代替。

## 练习 5：理解 `scalar` 和 `scalars`

在 `/users` 里分别写出这两句：

```python
total = session.scalar(select(func.count()).select_from(User))
users = session.scalars(select(User)).all()
```

然后用注释写出它们分别返回什么：

```python
# total 是一个 int，例如 5
# users 是 User 对象列表，例如 [User(...), User(...)]
```

要求：不要只会写，要能解释给自己听。

## 练习 6：分页超过范围

请求：

```text
GET /users?page=999&page_size=2
```

要求：

- 不报错。
- 返回空 `items`。
- `total` 仍然是真实总数。

思考：

```text
page 超过范围，是错误，还是正常空结果？
```

建议答案：对普通列表页来说，返回空结果通常可以接受；除非产品要求页码越界返回 400。

## 练习 7：排序白名单

让 `sort_by` 支持：

```text
name / email / active / created_at
```

要求：

```python
SortBy = Literal["name", "email", "active", "created_at"]
```

然后用映射表：

```python
sort_mapping = {
    "name": User.name,
    "email": User.email,
    "active": User.active,
    "created_at": User.created_at,
}
```

不要直接把字符串塞进 `order_by`。

原因：真实项目里这会带来无效字段或 SQL 注入风险。

## 练习 8：desc 排序

新增参数：

```python
sort_order: Literal["asc", "desc"] = Query("asc")
```

要求：

```python
sort_column = sort_mapping[sort_by]
ordered_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()
```

请求示例：

```text
GET /users?sort_by=name&sort_order=desc
```

预期：名字从 Z 到 A 排。

## 练习 9：写一段查询流程注释

在 `/users` 里写一段注释，说明顺序：

```text
1. 收集 where 条件
2. count total
3. order_by 排序
4. offset/limit 分页
5. user_to_dict 输出
```

这个顺序很重要：分页必须在过滤和排序之后。

## 练习 10：手写一遍不用看答案

关掉 `main.py`，只看下面提示，重新写一个最小版 `/users`：

- 参数：`page`、`page_size`、`active`
- 返回：`items`、`total`
- 数据：真实 SQLite + SQLAlchemy
- 查询：`select(User)`
- 总数：`func.count()`
- 当前页：`offset/limit`

写完后再对照 `main.py`。

## 自测清单

完成后你应该能回答：

- `execute()` 返回什么？
- `scalars()` 返回什么？
- `scalar()` 返回什么？
- `total` 为什么不能用 `len(items)`？
- `offset = (page - 1) * page_size` 为什么这么算？
- 为什么排序要用白名单映射？
- 为什么分页要在过滤和排序之后？
