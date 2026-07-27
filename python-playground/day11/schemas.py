from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["frontend", "backend", "tester", "pm"]


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    role: Role


class UserUpdateRole(BaseModel):
    role: Role


class UserPublic(BaseModel):
    id: int
    name: str
    role: Role
    active: bool


class ReportPublic(BaseModel):
    total: int
    active_count: int
    role_count: dict[str, int]
