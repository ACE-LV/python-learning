# red-back-end SQLAlchemy 写法对照表

这份文档按 `red-back-end` 的真实版本整理，只记录当前项目推荐的 SQLAlchemy 2.x 写法。

核对结果：

```text
red-back-end/.venv Python  = 3.8.10
red-back-end SQLAlchemy    = 2.0.43
red-back-end FastAPI       = 0.117.1
red-back-end Pydantic      = 2.10.6
```

项目事实：

```text
模型层：SQLAlchemy 2.x typed mapping
主会话：AsyncSession
主查询：select(...) + await session.execute/scalars/scalar
```

所以日常记忆直接按 `select(...) + AsyncSession` 这套写。

## 0. Python 3.8 写法提醒

Python 3.8 项目里，类型标注优先用这些：

```python
from typing import Any, Dict, List, Optional

name: Optional[str]
users: List[User]
data: Dict[str, Any]
```

`red-back-end` 里很多文件有：

```python
from __future__ import annotations
```

这能让部分新式 annotation 延迟解析，但为了少踩坑，学习和日常维护时先用 `Optional` / `List` / `Dict` 更稳。

## 1. red-back-end 的模型写法

原生 SQL 表：

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  role VARCHAR(20) NOT NULL
);
```

red-back-end / SQLAlchemy 2.x 模型：

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
```

形象记忆：

```text
DeclarativeBase = ORM 表模型的总登记处
Mapped[...]     = 这个 Python 属性是数据库字段
mapped_column   = 字段的 SQL 类型和约束
```

## 2. red-back-end 的 Session 心智模型

项目主入口在 `red-back-end/app/core/db.py`：

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(...)
SessionFactory = async_sessionmaker(..., class_=AsyncSession)
```

FastAPI 接口通常拿到的是：

```python
session: AsyncSession
```

形象理解：

```text
engine  = 数据库连接工厂
session = 一次数据库操作窗口
select  = 先拼 SQL
await   = 真正去数据库执行
```

最重要的一句：

```text
select / where / order_by / limit 是在拼 SQL；await session.execute/scalars/scalar 才是真正执行。
```

## 2.1 本文示例数据

后面所有返回 demo 都先按这两张表理解。

第 1 节的 `User` 模型是最小示例；这里额外放了 `active`、`email`、`deleted_at`，只是为了演示后面的条件过滤、`COUNT` 和 `NULL` 查询。

`users`：

| id | name  | role    | active | email             | deleted_at |
| -- | ----- | ------- | ------ | ----------------- | ---------- |
| 1  | Alice | admin   | true   | alice@example.com | NULL       |
| 2  | Bob   | user    | true   | ""                | NULL       |
| 3  | Cindy | manager | false  | NULL              | 2026-01-01 |
| 4  | Alex  | admin   | true   | alex@example.com  | NULL       |

`orders`：

| id  | user_id | amount |
| --- | ------- | ------ |
| 101 | 1       | 120    |
| 102 | 1       | 80     |
| 103 | 2       | 50     |
| 104 | 4       | 200    |

先记住这个总区别：

```text
SQL 返回的是表格行。
SQLAlchemy 取结果时，返回形态由 execute / scalar / scalars 决定。

select(User) + scalars -> [User(...), User(...)]
select(User.id, User.name) + execute -> [(1, "Alice"), (2, "Bob")]
select(User.name) + scalars -> ["Alice", "Bob"]
select(func.count(...)) + scalar -> 4
```

## 3. 查全部

SQL：

```sql
SELECT *
FROM users;
```

red-back-end 推荐 async 写法：

```python
from sqlalchemy import select

stmt = select(User)
users = (await session.scalars(stmt)).all()
```

记忆：

```text
select(User)          = SELECT users.* FROM users
session.scalars(stmt) = 每行只拿 User 对象
.all()                = 拿所有结果
```

返回 demo：

```python
users == [
    User(id=1, name="Alice", role="admin", active=True),
    User(id=2, name="Bob", role="user", active=True),
    User(id=3, name="Cindy", role="manager", active=False),
    User(id=4, name="Alex", role="admin", active=True),
]
```

这里拿到的是 ORM 对象，所以可以 `users[0].name`，也能被 `session` 追踪修改。

## 4. 按主键查一条

SQL：

```sql
SELECT *
FROM users
WHERE id = 1;
```

red-back-end async 写法：

```python
user = await session.get(User, 1)
```

也可以写：

```python
stmt = select(User).where(User.id == 1)
user = await session.scalar(stmt)
```

记忆：

```text
只按主键 id 找一条 -> session.get(Model, id)
复杂条件查一条     -> select(...).where(...) + scalar
```

返回 demo：

```python
user == User(id=1, name="Alice", role="admin", active=True)
```

如果没有 `id = 1` 这条数据：

```python
user is None
```

## 5. 普通条件查一条

SQL：

```sql
SELECT *
FROM users
WHERE name = 'Alice'
LIMIT 1;
```

red-back-end async：

```python
stmt = select(User).where(User.name == "Alice")
user = await session.scalar(stmt)
```

如果你想明确只拿第一条：

```python
result = await session.scalars(stmt)
user = result.first()
```

记忆：

```text
where(...) = SQL WHERE
scalar(...) = 拿第一行第一列；select(User) 时第一列就是 User 对象
```

返回 demo：

```python
user == User(id=1, name="Alice", role="admin", active=True)
```

如果结果有多条，`scalar(stmt)` 也是拿第一行第一列；没有 `order_by` 时，“第一条”不保证稳定。

## 6. 多条件 AND

SQL：

```sql
SELECT *
FROM users
WHERE role = 'admin'
  AND active = 1;
```

red-back-end async：

```python
stmt = select(User).where(
    User.role == "admin",
    User.active == True,
)
users = (await session.scalars(stmt)).all()
```

也可以动态收集条件：

```python
conditions = []

if role is not None:
    conditions.append(User.role == role)

if active is not None:
    conditions.append(User.active == active)

stmt = select(User).where(*conditions)
users = (await session.scalars(stmt)).all()
```

记忆：

```text
where(A, B) = A AND B
where(*conditions) = 把条件列表展开成 AND
```

返回 demo：

```python
users == [
    User(id=1, name="Alice", role="admin", active=True),
    User(id=4, name="Alex", role="admin", active=True),
]
```

## 7. OR 条件

SQL：

```sql
SELECT *
FROM users
WHERE role = 'admin'
   OR role = 'manager';
```

red-back-end async：

```python
from sqlalchemy import or_

stmt = select(User).where(
    or_(User.role == "admin", User.role == "manager")
)
users = (await session.scalars(stmt)).all()
```

记忆：

```text
AND 可以直接多个 where 条件
OR 要明确写 or_(...)
```

返回 demo：

```python
users == [
    User(id=1, name="Alice", role="admin", active=True),
    User(id=3, name="Cindy", role="manager", active=False),
    User(id=4, name="Alex", role="admin", active=True),
]
```

## 8. IN / NOT IN

SQL：

```sql
SELECT *
FROM users
WHERE role IN ('admin', 'manager');
```

red-back-end async：

```python
roles = ["admin", "manager"]
stmt = select(User).where(User.role.in_(roles))
users = (await session.scalars(stmt)).all()
```

NOT IN：

```python
stmt = select(User).where(~User.role.in_(roles))
```

记忆：

```text
in_(list) = SQL IN
~         = SQL NOT
```

返回 demo：

```python
users == [
    User(id=1, name="Alice", role="admin", active=True),
    User(id=3, name="Cindy", role="manager", active=False),
    User(id=4, name="Alex", role="admin", active=True),
]
```

## 9. LIKE 模糊搜索

SQL：

```sql
SELECT *
FROM users
WHERE name LIKE '%ali%';
```

red-back-end async：

```python
keyword = "ali"
stmt = select(User).where(User.name.like("%{}%".format(keyword)))
users = (await session.scalars(stmt)).all()
```

大小写不敏感写法：

```python
from sqlalchemy import func

stmt = select(User).where(
    func.lower(User.name).contains(keyword.lower())
)
users = (await session.scalars(stmt)).all()
```

记忆：

```text
like('%x%')      = 包含 x
like('x%')       = 以 x 开头
like('%x')       = 以 x 结尾
func.lower(...)  = 转小写后比较
```

返回 demo：

```python
users == [
    User(id=1, name="Alice", role="admin", active=True),
]
```

如果数据库的 `LIKE` 区分大小写，优先用上面的 `func.lower(...)` 写法。

## 10. NULL / NOT NULL

SQL：

```sql
SELECT *
FROM users
WHERE deleted_at IS NULL;
```

red-back-end async：

```python
stmt = select(User).where(User.deleted_at.is_(None))
users = (await session.scalars(stmt)).all()
```

SQL：

```sql
SELECT *
FROM users
WHERE deleted_at IS NOT NULL;
```

red-back-end async：

```python
stmt = select(User).where(User.deleted_at.is_not(None))
users = (await session.scalars(stmt)).all()
```

兼容老写法也常见：

```python
User.deleted_at.isnot(None)
```

记忆：

```text
SQL 里 NULL 不用 = NULL
SQLAlchemy 里用 is_(None) / is_not(None)
```

返回 demo：

```python
# deleted_at IS NULL
users == [
    User(id=1, name="Alice"),
    User(id=2, name="Bob"),
    User(id=4, name="Alex"),
]

# deleted_at IS NOT NULL
users == [
    User(id=3, name="Cindy"),
]
```

## 11. ORDER BY 排序

SQL：

```sql
SELECT *
FROM users
ORDER BY id DESC;
```

red-back-end async：

```python
stmt = select(User).order_by(User.id.desc())
users = (await session.scalars(stmt)).all()
```

多个排序：

```python
stmt = select(User).order_by(User.role.asc(), User.id.desc())
```

前端传排序字段时，不要直接拼字符串，使用白名单：

```python
sort_mapping = {
    "id": User.id,
    "name": User.name,
    "role": User.role,
}

sort_column = sort_mapping[sort_by]
ordered_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()
stmt = select(User).order_by(ordered_column)
```

记忆：

```text
order_by = 排队
asc      = A 到 Z / 小到大
desc     = Z 到 A / 大到小
```

返回 demo：

```python
users == [
    User(id=4, name="Alex"),
    User(id=3, name="Cindy"),
    User(id=2, name="Bob"),
    User(id=1, name="Alice"),
]
```

## 12. LIMIT / OFFSET 分页

SQL：

```sql
SELECT *
FROM users
ORDER BY id ASC
LIMIT 10 OFFSET 20;
```

red-back-end async：

```python
page = 3
page_size = 10
offset = (page - 1) * page_size

stmt = (
    select(User)
    .order_by(User.id.asc())
    .offset(offset)
    .limit(page_size)
)
users = (await session.scalars(stmt)).all()
```

记忆：

```text
page=1 -> offset=0
page=2 -> offset=10
page=3 -> offset=20

limit  = 拿多少条
offset = 跳过多少条
```

前端类比：

```javascript
users.slice(offset, offset + pageSize)
```

返回 demo：

```python
# 如果 page = 2, page_size = 2，并按 id ASC 排序
users == [
    User(id=3, name="Cindy"),
    User(id=4, name="Alex"),
]
```

## 13. COUNT 总数

SQL：

```sql
SELECT COUNT(*)
FROM users
WHERE active = 1;
```

red-back-end async：

```python
from sqlalchemy import func, select

stmt = select(func.count()).select_from(User).where(User.active == True)
total = await session.scalar(stmt) or 0
```

如果要数某个字段：

```python
stmt = select(func.count(User.id)).where(User.active == True)
total = await session.scalar(stmt) or 0
```

记忆：

```text
total = 过滤后、分页前的总数量
不要用 len(items) 当 total
```

返回 demo：

```python
total == 3
```

因为 `active = true` 的用户是 Alice、Bob、Alex。

如果数某个字段，`COUNT(column)` 只排除 `NULL`，不排除空字符串：

```python
email_total = await session.scalar(
    select(func.count(User.email)).where(User.active == True)
) or 0

email_total == 3
```

这里 Bob 的 `email = ""` 是空字符串，不是 `NULL`，所以会被统计。

## 14. 列表页组合模板

SQL 思路：

```sql
SELECT *
FROM users
WHERE name LIKE '%ali%'
  AND active = 1
ORDER BY id DESC
LIMIT 10 OFFSET 0;

SELECT COUNT(*)
FROM users
WHERE name LIKE '%ali%'
  AND active = 1;
```

red-back-end async 模板：

```python
from sqlalchemy import func, select


async def list_users(session, keyword=None, active=None, page=1, page_size=10):
    conditions = []

    if keyword:
        conditions.append(func.lower(User.name).contains(keyword.lower()))

    if active is not None:
        conditions.append(User.active == active)

    total_stmt = select(func.count()).select_from(User).where(*conditions)
    total = await session.scalar(total_stmt) or 0

    offset = (page - 1) * page_size
    items_stmt = (
        select(User)
        .where(*conditions)
        .order_by(User.id.desc())
        .offset(offset)
        .limit(page_size)
    )
    items = (await session.scalars(items_stmt)).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
```

口诀：

```text
先收条件，再 count；
再排序，再分页；
items 当前页，total 总数量。
```

返回 demo：

```python
await list_users(session, keyword="ali", active=True, page=1, page_size=10)

{
    "items": [User(id=1, name="Alice", role="admin", active=True)],
    "total": 1,
    "page": 1,
    "page_size": 10,
}
```

## 15. 只查部分字段

SQL：

```sql
SELECT id, name
FROM users;
```

red-back-end async：

```python
stmt = select(User.id, User.name)
rows = (await session.execute(stmt)).all()

for user_id, name in rows:
    print(user_id, name)
```

1记忆：

```text
select(User)               -> 用 scalars，拿 User 对象
select(User.id, User.name) -> 用 execute，拿 Row / tuple-like 结果
```

返回 demo：

```python
rows == [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Cindy"),
    (4, "Alex"),
]

rows[0].id == 1
rows[0].name == "Alice"
```

这里不是 `User` 对象，只是 Row。你可以读 `row.id`，但不能把它当 ORM 实体修改后 `commit()`。

## 16. scalar / scalars / execute 怎么选

查一个数字：

```python
total = await session.scalar(select(func.count()).select_from(User))
```

查一条 ORM 对象：

```python
user = await session.scalar(select(User).where(User.id == 1))
```

查多个 ORM 对象：

```python
users = (await session.scalars(select(User))).all()
```

查多个字段：

```python
rows = (await session.execute(select(User.id, User.name))).all()
```

速记：

```text
scalar  = 一个值
scalars = 一列值 / 一批 ORM 对象
execute = 多列 Row 结果
```

返回 demo 总览：

```python
await session.scalar(select(func.count()).select_from(User))
# 4

await session.scalar(select(User).where(User.id == 1))
# User(id=1, name="Alice", role="admin", active=True)

(await session.scalars(select(User))).all()
# [User(id=1, ...), User(id=2, ...), User(id=3, ...), User(id=4, ...)]

(await session.scalars(select(User.name))).all()
# ["Alice", "Bob", "Cindy", "Alex"]

(await session.execute(select(User.id, User.name))).all()
# [(1, "Alice"), (2, "Bob"), (3, "Cindy"), (4, "Alex")]
```

容易踩坑的写法：

```python
(await session.scalars(select(User.id, User.name))).all()
# [1, 2, 3, 4]
```

因为 `scalars()` 只拿每一行的第一列，`User.name` 会被丢掉。

## 17. first / one / one_or_none / all

red-back-end async：

```python
result = await session.scalars(select(User).where(User.role == "admin"))
```

```python
users = result.all()
```

返回列表。

```python
user = result.first()
```

返回第一条，没有就 `None`。

如果使用 `execute`：

```python
result = await session.execute(select(User).where(User.name == "Alice"))
user = result.scalar_one_or_none()
```

常见语义：

```text
all()                = 多条列表
first()              = 第一条或 None
scalar_one()         = 必须刚好一条，不然报错
scalar_one_or_none() = 0 或 1 条可以，多条报错
```

返回 demo：

```python
result = await session.scalars(select(User).where(User.role == "admin"))

result.all()
# [User(id=1, name="Alice"), User(id=4, name="Alex")]
```

注意 `result` 消费一次就不能再重复拿。想看 `first()`，要重新执行一次：

```python
result = await session.scalars(select(User).where(User.role == "admin"))

result.first()
# User(id=1, name="Alice")
```

没有 `order_by` 时，`first()` 的第一条不保证稳定。

## 18. INSERT 新增

SQL：

```sql
INSERT INTO users (name, role)
VALUES ('Alice', 'admin');
```

red-back-end async：

```python
user = User(name="Alice", role="admin")

session.add(user)
await session.commit()
await session.refresh(user)
```

记忆：

```text
Model(...)       = 创建 Python 对象
session.add(...) = 放进待写入队列
commit()         = 真正写入数据库
refresh()        = 从数据库读回最新值，比如 id
```

## 19. 批量 INSERT

SQL：

```sql
INSERT INTO users (name, role)
VALUES ('Alice', 'admin'), ('Bob', 'user');
```

red-back-end async 对象写法：

```python
session.add_all(
    [
        User(name="Alice", role="admin"),
        User(name="Bob", role="user"),
    ]
)
await session.commit()
```

更偏批处理的写法：

```python
from sqlalchemy import insert

await session.execute(
    insert(User),
    [
        {"name": "Alice", "role": "admin"},
        {"name": "Bob", "role": "user"},
    ],
)
await session.commit()
```

记忆：

```text
add_all       = ORM 对象批量新增
insert(Model) = 更像直接 SQL 批量插入
```

## 20. UPDATE：先查再改

SQL：

```sql
UPDATE users
SET name = 'Alice New'
WHERE id = 1;
```

red-back-end async：

```python
user = await session.get(User, 1)
if user is None:
    raise ValueError("User not found")

user.name = "Alice New"
await session.commit()
```

记忆：

```text
查对象 -> 改属性 -> commit
```

这像前端改 state：

```javascript
user.name = 'Alice New'
```

区别是 ORM 对象被 Session 追踪，`commit()` 时 SQLAlchemy 会生成 UPDATE。

## 21. 批量 UPDATE

SQL：

```sql
UPDATE users
SET active = 0
WHERE role = 'guest';
```

red-back-end async：

```python
from sqlalchemy import update

stmt = (
    update(User)
    .where(User.role == "guest")
    .values(active=False)
)
await session.execute(stmt)
await session.commit()
```

记忆：

```text
改一条并要做业务判断 -> get/select 找对象再改
批量状态变更         -> update(Model).where(...).values(...)
```

## 22. DELETE：先查再删

SQL：

```sql
DELETE FROM users
WHERE id = 1;
```

red-back-end async：

```python
user = await session.get(User, 1)
if user is None:
    raise ValueError("User not found")

await session.delete(user)
await session.commit()
```

记忆：

```text
查对象 -> delete(obj) -> commit
```

## 23. 批量 DELETE

SQL：

```sql
DELETE FROM users
WHERE active = 0;
```

red-back-end async：

```python
from sqlalchemy import delete

stmt = delete(User).where(User.active == False)
await session.execute(stmt)
await session.commit()
```

项目里更常见的是软删除字段：

```text
is_deleted = True
```

所以真实业务里先确认是不是应该软删除，而不是真的 `DELETE`。

## 24. GROUP BY 分组统计

SQL：

```sql
SELECT role, COUNT(*) AS total
FROM users
GROUP BY role;
```

red-back-end async：

```python
stmt = (
    select(User.role, func.count(User.id).label("total"))
    .group_by(User.role)
)
rows = (await session.execute(stmt)).all()

for role, total in rows:
    print(role, total)
```

记忆：

```text
select(分组字段, 聚合函数)
.group_by(分组字段)
```

返回 demo：

```python
rows == [
    ("admin", 2),
    ("manager", 1),
    ("user", 1),
]
```

这里是两个字段，所以用 `execute()`，返回 Row / tuple-like 结果。

## 25. HAVING 分组后筛选

SQL：

```sql
SELECT role, COUNT(*) AS total
FROM users
GROUP BY role
HAVING COUNT(*) > 1;
```

red-back-end async：

```python
stmt = (
    select(User.role, func.count(User.id).label("total"))
    .group_by(User.role)
    .having(func.count(User.id) > 1)
)
rows = (await session.execute(stmt)).all()
```

记忆：

```text
WHERE  = 分组前筛选行
HAVING = 分组后筛选组
```

返回 demo：

```python
rows == [
    ("admin", 2),
]
```

因为只有 `admin` 分组数量大于 1。

## 26. JOIN

假设有订单表：

```python
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)
```

SQL：

```sql
SELECT users.name, orders.amount
FROM users
JOIN orders ON orders.user_id = users.id;
```

red-back-end async：

```python
stmt = (
    select(User.name, Order.amount)
    .join(Order, Order.user_id == User.id)
)
rows = (await session.execute(stmt)).all()
```

LEFT JOIN：

```python
stmt = (
    select(User.name, Order.amount)
    .outerjoin(Order, Order.user_id == User.id)
)
rows = (await session.execute(stmt)).all()
```

记忆：

```text
join      = INNER JOIN
outerjoin = LEFT JOIN
```

返回 demo：

```python
# JOIN：只返回匹配到订单的用户行
rows == [
    ("Alice", 120),
    ("Alice", 80),
    ("Bob", 50),
    ("Alex", 200),
]

# LEFT JOIN：保留左表 users；没有订单的 Cindy，订单金额是 None
rows == [
    ("Alice", 120),
    ("Alice", 80),
    ("Bob", 50),
    ("Cindy", None),
    ("Alex", 200),
]
```

只查 `User.name, Order.amount` 是 Row；如果写 `select(User).join(...)` 再配 `scalars()`，才会拿 User ORM 对象。

## 27. DISTINCT 去重

SQL：

```sql
SELECT DISTINCT role
FROM users;
```

red-back-end async：

```python
from sqlalchemy import distinct

stmt = select(distinct(User.role))
roles = (await session.scalars(stmt)).all()
```

也可以：

```python
stmt = select(User.role).distinct()
roles = (await session.scalars(stmt)).all()
```

返回 demo：

```python
roles == ["admin", "user", "manager"]
```

没有 `order_by` 时，去重后的顺序不保证稳定。

## 28. EXISTS / 是否存在

SQL：

```sql
SELECT EXISTS (
  SELECT 1
  FROM users
  WHERE name = 'Alice'
);
```

red-back-end 日常简单写法：

```python
stmt = select(User.id).where(User.name == "Alice").limit(1)
exists_user = (await session.scalar(stmt)) is not None
```

更 SQL 风格：

```python
stmt = select(select(User).where(User.name == "Alice").exists())
exists_user = await session.scalar(stmt)
```

记忆：日常判断存在，`select(id).limit(1)` 更容易读。

返回 demo：

```python
# name = "Alice"
exists_user == True

# name = "Nobody"
exists_user == False
```

## 29. 原生 SQL text

SQL：

```sql
SELECT *
FROM users
WHERE role = :role;
```

red-back-end async：

```python
from sqlalchemy import text

stmt = text("SELECT * FROM users WHERE role = :role")
rows = (await session.execute(stmt, {"role": "admin"})).all()
```

不要字符串拼接：

```python
sql = "SELECT * FROM users WHERE role = '{}'".format(role)
```

原因：有 SQL 注入风险。

记忆：

```text
text(...) = 必须手写 SQL 时才用
:role     = 参数占位
```

返回 demo：

```python
rows == [
    (1, "Alice", "admin", True, "alice@example.com", None),
    (4, "Alex", "admin", True, "alex@example.com", None),
]
```

`text("SELECT * ...")` 返回的是原生 Row，不会自动组装成 `User` ORM 对象。

## 30. 最常用速记表

| 目标       | red-back-end 推荐写法                                            |
| ---------- | ---------------------------------------------------------------- |
| 查全部对象 | `(await session.scalars(select(User))).all()`                  |
| 按主键查   | `await session.get(User, user_id)`                             |
| 条件查一条 | `await session.scalar(select(User).where(...))`                |
| 条件查多条 | `(await session.scalars(select(User).where(...))).all()`       |
| 查多字段   | `(await session.execute(select(User.id, User.name))).all()`    |
| AND        | `.where(A, B)` 或 `.where(*conditions)`                      |
| OR         | `.where(or_(A, B))`                                            |
| IN         | `.where(User.role.in_(roles))`                                 |
| LIKE       | `.where(User.name.like("%{}%".format(keyword)))`               |
| NULL       | `.where(User.deleted_at.is_(None))`                            |
| 排序       | `.order_by(User.id.desc())`                                    |
| 分页       | `.offset(offset).limit(page_size)`                             |
| count      | `await session.scalar(select(func.count()).select_from(User))` |
| 新增       | `session.add(obj); await session.commit()`                     |
| 修改       | `obj.name = "x"; await session.commit()`                       |
| 删除对象   | `await session.delete(obj); await session.commit()`            |
| 批量更新   | `await session.execute(update(User).where(...).values(...))`   |
| 批量删除   | `await session.execute(delete(User).where(...))`               |
| 分组       | `.group_by(User.role)`                                         |
| 分组筛选   | `.having(func.count(User.id) > 1)`                             |
| 关联       | `.join(Order, Order.user_id == User.id)`                       |
| 左关联     | `.outerjoin(Order, Order.user_id == User.id)`                  |
| 原生 SQL   | `await session.execute(text("..."), params)`                   |

## 31. 最终形象记忆

把 SQLAlchemy 2.x 查询想成“先写查询计划，再让 session 执行”：

```text
select(User)
      ↓
我要查 users 表对应的 User 对象

.where(...)
      ↓
加 WHERE 条件

.order_by(...)
      ↓
加 ORDER BY 排序

.offset(...).limit(...)
      ↓
加分页

await session.scalars(stmt)
      ↓
真正发 SQL，并只取每行的 User 对象

.all()
      ↓
转成列表
```

CRUD 口诀：

```text
查：select + await session.scalar/scalars/execute
增：Model(...) + session.add + await commit
改：get/select 找对象 + 改属性 + await commit
删：get/select 找对象 + await delete + await commit
```

分页口诀：

```text
先过滤，再 count；
再排序，再分页；
items 当前页，total 总数量。
```

版本口诀：

```text
red-back-end = Python 3.8 + SQLAlchemy 2.0 + AsyncSession
新写接口逻辑 = select(...) + await session.xxx(...)
```
