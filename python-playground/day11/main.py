from fastapi import FastAPI, HTTPException

from . import services
from .schemas import ReportPublic, UserCreate, UserPublic, UserUpdateRole

app = FastAPI(title="Day11 API Layers")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users", response_model=list[UserPublic])
def list_users() -> list[object]:
    return services.list_users()


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int) -> object:
    user = services.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=UserPublic)
def create_user(payload: UserCreate) -> object:
    return services.create_user(payload)


@app.patch("/users/{user_id}/role", response_model=UserPublic)
def update_user_role(user_id: int, payload: UserUpdateRole) -> object:
    user = services.update_user_role(user_id, payload.role)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}/deactivate", response_model=UserPublic)
def deactivate_user(user_id: int) -> object:
    user = services.deactivate_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, bool]:
    if not services.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}


@app.get("/report", response_model=ReportPublic)
def get_report() -> dict[str, object]:
    return services.build_report()
