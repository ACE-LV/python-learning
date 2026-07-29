from collections import Counter

from .models import User
from .schemas import UserCreate

# services.py 放业务逻辑。
# 路由层 main.py 不直接操作 USERS，而是调用这些函数；这样 main.py 可以保持很薄。

# 这里用内存列表模拟数据库。
# 真实项目里，这一层通常会改成调用数据库 repository / ORM session。
USERS: list[User] = [
    User(id=1, name="Alice", role="frontend"),
    User(id=2, name="Bob", role="backend"),
]

# 模拟自增主键。每创建一个用户，就用 NEXT_ID，然后自增。
NEXT_ID = 3


def list_users() -> list[User]:
    # 查询所有用户。
    # 为什么返回 User 对象：service 层面向内部业务对象，API 输出格式交给 response_model 处理。
    return USERS


def get_user(user_id: int) -> User | None:
    # 根据 id 查找用户。
    # 找不到返回 None，不在 service 里直接抛 HTTPException。
    # 为什么：service 不应该绑定 HTTP 细节；404 是 API 层 main.py 的责任。
    return next((user for user in USERS if user.id == user_id), None)


def create_user(payload: UserCreate) -> User:
    # 创建用户。
    # payload 已经在 API 层被 Pydantic 校验过，所以这里可以直接使用 payload.name / payload.role。
    global NEXT_ID

    user = User(id=NEXT_ID, name=payload.name, role=payload.role)
    USERS.append(user)
    NEXT_ID += 1
    return user


def update_user_role(user_id: int, role: str) -> User | None:
    # 更新用户角色。
    # 找不到用户时仍然返回 None，由 main.py 决定转成 404。
    user = get_user(user_id)
    if user is None:
        return None
    user.role = role
    return user


def deactivate_user(user_id: int) -> User | None:
    # 软删除/停用用户：不从列表移除，只把 active 改成 False。
    # 适合需要保留历史记录的业务场景。
    user = get_user(user_id)
    if user is None:
        return None
    user.active = False
    return user


def delete_user(user_id: int) -> bool:
    # 硬删除用户：直接从 USERS 列表里移除。
    # 返回 bool 表示是否删除成功，main.py 根据 False 返回 404。
    user = get_user(user_id)
    if user is None:
        return False
    USERS.remove(user)
    return True


def build_report() -> dict[str, object]:
    # 构建用户统计报表。
    # Counter 会按 role 自动计数，类似 JS 里 reduce 统计分组数量。
    role_count = Counter(user.role for user in USERS)
    return {
        "total": len(USERS),
        "active_count": sum(1 for user in USERS if user.active),
        "role_count": dict(role_count),
    }
