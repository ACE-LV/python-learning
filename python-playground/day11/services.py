from collections import Counter

from .models import User
from .schemas import UserCreate

USERS: list[User] = [
    User(id=1, name="Alice", role="frontend"),
    User(id=2, name="Bob", role="backend"),
]
NEXT_ID = 3


def list_users() -> list[User]:
    return USERS


def get_user(user_id: int) -> User | None:
    return next((user for user in USERS if user.id == user_id), None)


def create_user(payload: UserCreate) -> User:
    global NEXT_ID

    user = User(id=NEXT_ID, name=payload.name, role=payload.role)
    USERS.append(user)
    NEXT_ID += 1
    return user


def update_user_role(user_id: int, role: str) -> User | None:
    user = get_user(user_id)
    if user is None:
        return None
    user.role = role
    return user


def deactivate_user(user_id: int) -> User | None:
    user = get_user(user_id)
    if user is None:
        return None
    user.active = False
    return user


def delete_user(user_id: int) -> bool:
    user = get_user(user_id)
    if user is None:
        return False
    USERS.remove(user)
    return True


def build_report() -> dict[str, object]:
    role_count = Counter(user.role for user in USERS)
    return {
        "total": len(USERS),
        "active_count": sum(1 for user in USERS if user.active),
        "role_count": dict(role_count),
    }
