from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel

# 第 12 天主题：给前端表格页提供标准查询接口。
# 前端表格常见需求：分页、搜索、筛选、排序，这些通常都通过 query 参数传给后端。
app = FastAPI(title="Day12 Pagination Search Sort")

# Role 限制 role 查询参数和响应字段只能是固定角色值。
Role = Literal["frontend", "backend", "tester", "pm"]

# SortBy 限制前端只能按这些字段排序，避免传入任意字段名。
# 如果允许任意 sort_by，真实项目里可能带来 SQL 注入或无效字段问题。
SortBy = Literal["id", "name", "role"]

# SortOrder 限制排序方向只能是升序 asc 或降序 desc。
SortOrder = Literal["asc", "desc"]


class UserPublic(BaseModel):
    # 单个用户返回结构。
    # PageResult.items 会复用它，保证列表里每条数据结构稳定。
    id: int
    name: str
    role: Role
    active: bool


class PageResult(BaseModel):
    # 前端表格页常见响应结构。
    # items 是当前页数据，不是全部数据。
    items: list[UserPublic]
    # total 是过滤/搜索后的总条数。
    # 前端需要它来计算总页数和显示 “1-10 of 28 items”。
    total: int
    # page/page_size 回显当前请求参数，方便前端确认当前页状态。
    page: int
    page_size: int
    # total_pages 是后端算好的总页数；前端也可以用 total/page_size 自己算。
    total_pages: int


# 用内存数据模拟数据库表。
# 真实项目里这里会变成数据库查询：先 where 过滤，再 order by 排序，再 limit/offset 分页。
USERS: list[dict[str, object]] = [
    {"id": 1, "name": "Alice", "role": "frontend", "active": True},
    {"id": 2, "name": "Bob", "role": "backend", "active": True},
    {"id": 3, "name": "Cindy", "role": "tester", "active": False},
    {"id": 4, "name": "Daniel", "role": "frontend", "active": True},
    {"id": 5, "name": "Eva", "role": "pm", "active": True},
    {"id": 6, "name": "Frank", "role": "backend", "active": False},
    {"id": 7, "name": "Grace", "role": "frontend", "active": True},
]


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口，用于确认服务启动。
    return {"status": "ok"}


@app.get("/users", response_model=PageResult)
def list_users(
    # page 是当前页，从 1 开始。
    # ge=1 表示必须 >= 1；如果 page=0，FastAPI 自动返回 422。
    page: int = Query(default=1, ge=1),

    # page_size 是每页条数。
    # ge=1/le=50 限制最小 1、最大 50，避免前端一次请求太多数据。
    page_size: int = Query(default=5, ge=1, le=50),

    # keyword 是可选搜索词。
    # None 表示前端没传 keyword，不做搜索。
    keyword: str | None = Query(default=None),

    # role 是可选筛选条件，且只能是 Role 定义的合法值。
    role: Role | None = Query(default=None),

    # active 是可选布尔筛选条件。
    # URL 里可以传 active=true 或 active=false。
    active: bool | None = Query(default=None),

    # sort_by / sort_order 控制排序。
    # 默认按 id 升序，保证结果顺序稳定。
    sort_by: SortBy = Query(default="id"),
    sort_order: SortOrder = Query(default="asc"),
) -> dict[str, object]:
    # copy 一份列表，避免下面过滤/排序直接改动全局 USERS 的顺序。
    rows = USERS.copy()

    # 1. 搜索：按 name 包含 keyword 过滤。
    # lower() 用来做不区分大小写搜索，例如 keyword=a 能匹配 Alice/Grace。
    if keyword:
        lowered_keyword = keyword.lower()
        rows = [user for user in rows if lowered_keyword in str(user["name"]).lower()]

    # 2. 角色筛选：只保留指定 role 的用户。
    if role is not None:
        rows = [user for user in rows if user["role"] == role]

    # 3. 启用状态筛选：只保留 active 状态匹配的用户。
    if active is not None:
        rows = [user for user in rows if user["active"] is active]

    # 4. 排序：必须在分页前做。
    # 如果先分页再排序，只会排序当前页，整体顺序会错。
    rows.sort(key=lambda user: user[sort_by], reverse=sort_order == "desc")

    # 5. total 必须在分页前计算。
    # total 表示过滤后的总条数，不是当前页 items 的数量。
    total = len(rows)

    # 6. 分页：把 page/page_size 转成列表切片范围。
    # page=1,page_size=5 -> start=0,end=5。
    # page=2,page_size=5 -> start=5,end=10。
    start = (page - 1) * page_size
    end = start + page_size
    items = rows[start:end]

    # 向上取整计算总页数。
    # 例如 total=7,page_size=5 -> (7+5-1)//5 = 2 页。
    total_pages = (total + page_size - 1) // page_size

    # 返回前端表格需要的标准分页结构。
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
