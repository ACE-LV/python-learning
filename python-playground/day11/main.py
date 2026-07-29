from fastapi import FastAPI, HTTPException

from . import services
from .schemas import ReportPublic, UserCreate, UserPublic, UserUpdateRole

# main.py 只负责 FastAPI 路由入口。
# 它不直接写业务规则，而是把请求交给 services.py，再把 service 结果转换成 HTTP 响应。
app = FastAPI(title="Day11 API Layers")


@app.get("/health")
def health_check() -> dict[str, str]:
    # 健康检查接口，只确认服务启动成功。
    return {"status": "ok"}


@app.get("/users", response_model=list[UserPublic])
def list_users() -> list[object]:
    # 路由层只调用 service，不关心 USERS 存在哪里。
    # response_model 会把 User dataclass 转成 UserPublic 规定的响应字段。
    return services.list_users()


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int) -> object:
    # 路径参数 user_id 由 FastAPI 自动解析成 int。
    user = services.get_user(user_id)
    if user is None:
        # service 返回 None，路由层把它翻译成 HTTP 404。
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=UserPublic)
def create_user(payload: UserCreate) -> object:
    # payload 是 Pydantic 校验后的请求体。
    # 非法 role 或空 name 会在进入函数前被 FastAPI 拦截，返回 422。
    return services.create_user(payload)


@app.patch("/users/{user_id}/role", response_model=UserPublic)
def update_user_role(user_id: int, payload: UserUpdateRole) -> object:
    # 只更新 role 的接口，所以请求体使用 UserUpdateRole，而不是 UserCreate。
    user = services.update_user_role(user_id, payload.role)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}/deactivate", response_model=UserPublic)
def deactivate_user(user_id: int) -> object:
    # 停用用户：保留用户记录，只把 active 改成 False。
    user = services.deactivate_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, bool]:
    # 删除用户：service 返回 False 表示目标不存在。
    if not services.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}


@app.get("/report", response_model=ReportPublic)
def get_report() -> dict[str, object]:
    # 报表接口：路由层只暴露 HTTP 入口，统计逻辑放在 service。
    return services.build_report()
