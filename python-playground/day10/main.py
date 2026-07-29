# Literal 用来限制字段只能取固定几个字符串值。
# 前端类比：type Role = "frontend" | "backend" | "tester" | "pm"。
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# FastAPI 应用实例。
# title 会显示在 Swagger /docs 页面顶部，方便你知道当前打开的是哪一天的练习服务。
app = FastAPI(title="Day10 Pydantic Validation")

# Role 是一个类型别名。
# 作用：把允许的角色值收拢到一个地方，后面多个模型可以复用。
# 为什么用 Literal：它不仅给编辑器类型提示，也会被 Pydantic/FastAPI 用来生成校验规则。
# 如果请求里传 role="admin"，FastAPI 会自动返回 422，因为 admin 不在允许范围内。
Role = Literal["frontend", "backend", "tester", "pm"]


class UserCreate(BaseModel):
    # BaseModel 是 Pydantic 的模型基类。
    # 这个类描述 POST /users 的请求体，也就是“创建用户时前端需要传什么”。
    # FastAPI 会自动把 JSON body 转成 UserCreate 对象，并按下面的类型和 Field 规则校验。

    # Field 用来给字段加运行时校验规则。
    # min_length=1：不能为空字符串。
    # max_length=50：最多 50 个字符。
    # 如果不满足，FastAPI 自动返回 422。
    name: str = Field(min_length=1, max_length=50)

    # role 必须是 Role 里定义的四个值之一。
    # 合法：frontend/backend/tester/pm。
    # 非法：admin/devops 等都会触发 422。
    role: Role

    # age 必须是整数，并且范围在 1 到 120。
    # ge 是 greater than or equal，大于等于。
    # le 是 less than or equal，小于等于。
    age: int = Field(ge=1, le=120)

    # active 有默认值 True，所以创建用户时可以不传。
    # 如果前端不传 active，Pydantic 会自动补成 True。
    active: bool = True


class UserUpdate(BaseModel):
    # 这个类描述 PATCH /users/{user_id} 的请求体。
    # PATCH 是“局部更新”，所以字段都允许为 None，表示“不更新这个字段”。

    # str | None 表示这个字段可以是字符串，也可以不传/为 None。
    # default=None 表示默认不更新 name。
    # 但只要传了 name，它仍然必须满足长度 1-50。
    name: str | None = Field(default=None, min_length=1, max_length=50)

    # role 不传就不更新；传了就必须是 Role 的合法值。
    role: Role | None = None

    # age 不传就不更新；传了就必须在 1-120 范围内。
    age: int | None = Field(default=None, ge=1, le=120)

    # active 不传就不更新；传了必须是布尔值。
    active: bool | None = None


class UserPublic(BaseModel):
    # 这个类描述接口“返回给前端”的用户结构。
    # 它通常叫 response DTO / response schema。
    # 为什么单独定义：后端内部数据可能有 password_hash、internal_note 等字段，
    # response_model=UserPublic 可以保证只返回这里列出的公开字段。
    id: int
    name: str
    role: Role
    age: int
    active: bool


# 这里用内存 list 模拟数据库。
# 真实项目里通常会换成 SQLAlchemy Session 查询数据库。
# list[dict[str, object]] 表示：USERS 是一个列表，列表每项是 dict。
USERS: list[dict[str, object]] = [
    {"id": 1, "name": "Alice", "role": "frontend", "age": 28, "active": True},
    {"id": 2, "name": "Bob", "role": "backend", "age": 32, "active": True},
]

# NEXT_ID 模拟数据库自增 ID。
# 每创建一个用户，就用当前 NEXT_ID 作为 id，然后加 1。
NEXT_ID = 3


def find_user(user_id: int) -> dict[str, object] | None:
    # 根据 id 在 USERS 里找用户。
    # next(..., None) 的意思是：找到第一个匹配项；如果找不到，就返回 None。
    # 返回 None 后，接口层会转成 404。
    return next((user for user in USERS if user["id"] == user_id), None)


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口。
    # 常用于确认服务是否启动成功，不涉及业务数据。
    return {"status": "ok"}


@app.get("/users", response_model=list[UserPublic])
def list_users(active: bool | None = Query(default=None)) -> list[dict[str, object]]:
    # response_model=list[UserPublic] 的作用：
    # 1. 告诉 FastAPI 这个接口返回 UserPublic 数组。
    # 2. 自动生成 Swagger 响应 schema。
    # 3. 返回前过滤掉 UserPublic 没定义的字段。

    # Query(default=None) 表示 active 是 URL 查询参数，不是请求体。
    # 例子：GET /users?active=true
    # active 是 None 时表示前端没有传这个筛选条件。
    if active is None:
        return USERS

    # 有 active 参数时，只返回 active 状态匹配的用户。
    return [user for user in USERS if user["active"] is active]


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int) -> dict[str, object]:
    # user_id 来自路径参数。
    # 例子：GET /users/1 会让 user_id = 1。
    user = find_user(user_id)
    if user is None:
        # 404 表示“请求格式没问题，但资源不存在”。
        # 和 422 不同：422 是请求参数格式/校验不通过。
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=UserPublic)
def create_user(payload: UserCreate) -> dict[str, object]:
    # payload 是经过 Pydantic 校验后的请求体对象。
    # 如果前端传入非法 name/role/age，函数体不会执行，FastAPI 会直接返回 422。

    # 因为下面要修改全局变量 NEXT_ID，所以需要 global 声明。
    global NEXT_ID

    # payload.dict() 把 Pydantic 对象转成普通 dict。
    # {"id": NEXT_ID, **payload.dict()} 等价于把 id 和用户提交的字段合并成一个新用户 dict。
    user = {"id": NEXT_ID, **payload.dict()}
    USERS.append(user)
    NEXT_ID += 1
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, payload: UserUpdate) -> dict[str, object]:
    # 先确认要更新的用户存在。
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # PATCH 是局部更新，所以只更新前端实际传了的字段。
    # exclude_none=True 会过滤掉值为 None 的字段。
    # 例如请求只传 {"age": 30}，这里就只更新 age，不影响 name/role/active。
    for key, value in payload.dict(exclude_none=True).items():
        user[key] = value
    return user
