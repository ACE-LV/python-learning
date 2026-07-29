from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 第 16 天主题：给 FastAPI 接口写自动化测试。
# main.py 提供被测试的 API，test_main.py 使用 TestClient 模拟 HTTP 请求。
app = FastAPI(title="Day16 FastAPI Tests")

# 用内存列表模拟数据库。
# 测试时不希望依赖真实数据库，这样测试更快、更稳定。
USERS: list[dict[str, object]] = []

# 模拟自增 ID。
NEXT_ID = 1


class UserCreate(BaseModel):
    # POST /users 的请求体。
    # Field 约束可以被测试覆盖：空 name 会返回 422。
    name: str = Field(min_length=1, max_length=50)
    role: str = Field(min_length=1, max_length=50)


def reset_users() -> None:
    # 重置测试数据。
    # 为什么需要：每个测试都应该独立运行，不依赖上一个测试新增/删除后的状态。
    # pytest fixture 会在每个测试前调用它。
    global NEXT_ID, USERS

    USERS = [{"id": 1, "name": "Alice", "role": "frontend"}]
    NEXT_ID = 2


def find_user(user_id: int) -> dict[str, object] | None:
    # 根据 id 查找用户，找不到返回 None。
    return next((user for user in USERS if user["id"] == user_id), None)


# 模块加载时先初始化一次数据，方便手动运行服务时也有默认用户。
reset_users()


@app.get("/health")
def health_check() -> dict[str, str]:
    # 用于测试服务是否能正常响应。
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict[str, object]]:
    # 返回当前所有用户。测试会断言初始数据只有 Alice。
    return USERS


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    # 成功场景返回用户；失败场景返回 404。
    # 自动化测试需要覆盖这两种情况。
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    # 创建用户接口。
    # 测试会覆盖合法 payload 返回 200，以及非法 payload 返回 422。
    global NEXT_ID

    user = {"id": NEXT_ID, "name": payload.name, "role": payload.role}
    USERS.append(user)
    NEXT_ID += 1
    return user
