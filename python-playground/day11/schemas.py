from typing import Literal

from pydantic import BaseModel, Field

# schemas.py 放“接口边界的数据形状”。
# 前端类比：这里像 TypeScript 的 request/response DTO，但 Pydantic 会在运行时真正校验。

# Role 是接口允许的角色枚举。
# 为什么放在 schemas.py：它属于 API 入参/出参约束，不属于内部业务存储结构。
Role = Literal["frontend", "backend", "tester", "pm"]


class UserCreate(BaseModel):
    # POST /users 的请求体。
    # name 必填，并且长度必须在 1-50 之间；不满足时 FastAPI 自动返回 422。
    name: str = Field(min_length=1, max_length=50)
    # role 必须是 Role 中的值；比如 admin 会被拒绝。
    role: Role


class UserUpdateRole(BaseModel):
    # PATCH /users/{user_id}/role 的请求体。
    # 单独建一个模型，是为了让更新角色接口只允许修改 role，不暴露其它字段。
    role: Role


class UserPublic(BaseModel):
    # 返回给前端看的用户结构。
    # response_model=UserPublic 会按这里的字段过滤输出，避免内部字段泄漏。
    id: int
    name: str
    role: Role
    active: bool


class ReportPublic(BaseModel):
    # GET /report 的响应结构。
    # 报表不是单个 User，所以单独定义一个 response schema。
    total: int
    # active_count 表示 active=True 的用户数量。
    active_count: int
    # role_count 是按角色分组的统计结果，例如 {"frontend": 2, "backend": 1}。
    role_count: dict[str, int]


class UserUpdate(BaseModel):
    # PATCH /users/{user_id} 的请求体。
    # 允许局部更新，所以字段都可以不传。
    name: str | None = Field(default=None, min_length=1, max_length=50)
