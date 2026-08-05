# Day12 写后端表格查询接口的流程

这份流程用于练习：真实数据库 + SQLAlchemy + FastAPI 查询接口。

目标不是一次写漂亮，而是卡住时知道下一步该写什么。

## 总流程

写一个表格查询接口时，按这个顺序来：

```text
1. 先定数据表模型
2. 再定返回给前端的 Response 模型
3. 准备数据库 engine / Base / init_db
4. 写一个对象转 dict 的函数
5. 写接口参数 Query
6. 收集筛选条件 conditions
7. 定义排序 sort_mapping
8. 先查 total
9. 再查当前页 items
10. 返回分页结构
```

不要一上来就写完整接口。每一步单独想。

## 第 1 步：先定数据表模型

先问自己：这张表要存什么？

比如用户表：

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

这一层回答的是：

```text
数据库里有哪些字段？
字段类型是什么？
字段能不能为空？
```

前端类比：这像后端自己的 data model，不是接口返回 DTO。

## 第 2 步：再定返回给前端的 Response 模型

问自己：前端应该看到什么？

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    active: bool
```

如果是分页接口，再定一个分页响应：

```python
class PageResult(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
```

这一层回答的是：

```text
接口最终返回什么形状？
前端表格需要哪些字段？
```

## 第 3 步：准备数据库连接

固定模板：

```python
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "xxx.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

然后准备 Base：

```python
class Base(DeclarativeBase):
    pass
```

启动时建表：

```python
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
```

## 第 4 步：写对象转 dict

不要直接返回 ORM 对象的 `__dict__`。

写一个干净的转换函数：

```python
def user_to_dict(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "active": user.active,
    }
```

这一层回答的是：

```text
数据库对象怎么变成 API 返回数据？
```

## 第 5 步：先写接口参数

先只想前端会传什么 params。

```python
@app.get("/users", response_model=PageResult)
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    active: bool | None = Query(default=None),
    keyword: str | None = Query(default=None),
    sort_by: SortBy = Query(default="id"),
    sort_order: SortOrder = Query(default="asc"),
) -> dict[str, object]:
    ...
```

前端对应：

```ts
request('/users', {
  method: 'GET',
  params: {
    page,
    page_size,
    active,
    keyword,
    sort_by,
    sort_order,
  },
})
```

## 第 6 步：收集筛选条件

固定写法：

```python
conditions = []

if active is not None:
    conditions.append(User.active == active)

if keyword:
    conditions.append(func.lower(User.name).contains(keyword.lower()))
```

记住：

```text
conditions 只是条件列表
还没有真正查询数据库
```

## 第 7 步：定义排序白名单

不要直接把前端传来的字符串塞进 `order_by`。

```python
sort_mapping = {
    "id": User.id,
    "name": User.name,
    "email": User.email,
    "active": User.active,
}

sort_column = sort_mapping[sort_by]
ordered_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()
```

为什么要白名单：

```text
防止无效字段
防止以后真实 SQL 场景出现注入风险
让前端能排序的字段明确可控
```

## 第 8 步：先查 total

分页接口一定要先算总数。

```python
with Session(engine) as session:
    total = session.scalar(
        select(func.count()).select_from(User).where(*conditions)
    ) or 0
```

脑图：

```text
select count(*)
from users
where 条件
```

注意：

```text
total 是过滤后的总条数
不是当前页 items 的长度
```

## 第 9 步：再查当前页 items

先算 offset：

```python
offset = (page - 1) * page_size
```

然后查当前页：

```python
stmt = (
    select(User)
    .where(*conditions)
    .order_by(ordered_column)
    .offset(offset)
    .limit(page_size)
)

rows = session.scalars(stmt).all()
```

脑图：

```text
select users
where 条件
order by 排序
skip offset 条
take page_size 条
```

## 第 10 步：返回分页结构

```python
total_pages = (total + page_size - 1) // page_size if total else 0

return {
    "items": [user_to_dict(user) for user in rows],
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages,
}
```

## 最小完整模板

```python
@app.get("/users", response_model=PageResult)
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    active: bool | None = Query(default=None),
    sort_by: SortBy = Query(default="id"),
    sort_order: SortOrder = Query(default="asc"),
) -> dict[str, object]:
    conditions = []
    if active is not None:
        conditions.append(User.active == active)

    sort_mapping = {
        "id": User.id,
        "name": User.name,
        "active": User.active,
    }
    sort_column = sort_mapping[sort_by]
    ordered_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()

    offset = (page - 1) * page_size

    with Session(engine) as session:
        total = session.scalar(
            select(func.count()).select_from(User).where(*conditions)
        ) or 0

        stmt = (
            select(User)
            .where(*conditions)
            .order_by(ordered_column)
            .offset(offset)
            .limit(page_size)
        )
        rows = session.scalars(stmt).all()

    total_pages = (total + page_size - 1) // page_size if total else 0
    return {
        "items": [user_to_dict(user) for user in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
```

## 卡住时按这个排查

### 不知道写什么参数

先问前端表格需要什么：

```text
当前页 page
每页条数 page_size
搜索 keyword
筛选 active/role
排序 sort_by/sort_order
```

### 不知道用 scalar 还是 scalars

```text
查一个数字 -> scalar
查一批 User 对象 -> scalars(...).all()
查多列 tuple -> execute(...).all()
```

### 不知道 total 怎么算

永远记住：

```text
total = 过滤后、分页前的数量
```

### 不知道分页怎么写

```python
offset = (page - 1) * page_size
limit = page_size
```

### 不知道排序怎么写

```python
sort_mapping = {"name": User.name}
ordered_column = sort_mapping[sort_by].desc()
```

## 推荐练习节奏

1. 只写 `GET /users/simple`，确认能查全部。
2. 加 `active` 筛选。
3. 加 `page/page_size`。
4. 加 `total`。
5. 加 `sort_by`。
6. 加 `sort_order`。
7. 最后再加 `keyword`。

每一步都能跑通后，再写下一步。
