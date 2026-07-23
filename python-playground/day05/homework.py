# 第五天作业
# 主题：用类封装一个用户管理器

# dataclass 让数据模型更简洁，适合 User 这种“字段为主”的对象。
from dataclasses import dataclass

print("=" * 30)
print("作业 1：定义 User dataclass")


# 任务：定义 User dataclass，字段：
# - user_id: int
# - name: str
# - role: str
# - active: bool = True
# 知识点：
# - 这是“数据模型层”。
# - active 设置默认值，创建对象时可不传。
@dataclass
class User:
    user_id: int
    name: str
    role: str
    active: bool = True


print("=" * 30)
print("作业 2：定义 UserManager 类")

# 任务：定义 UserManager，要求：
# - __init__ 接收 users: list[User]
# - get_total_users() -> int
# - get_active_users() -> list[User]
# - get_frontend_users() -> list[User]
# - count_by_role() -> dict[str, int]
# 知识点：
# - UserManager 是“行为层/服务层”，负责组织业务逻辑。
# - __init__ 里把 users 保存到 self.users，供其他方法复用。


class UserManager:
    def __init__(self, users: list[User]):
        self.users = users

    def get_total_users(self) -> int:
        return len(self.users)

    def get_active_users(self) -> list[User]:
        return [item for item in self.users if item.active == True]

    def get_frontend_user(self) -> list[User]:
        return [item for item in self.users if item.role == "frontend"]

    def count_by_role(self) -> dict[str, int]:
        role = {}
        for item in self.users:
            role[item.role] = role.get(item.role, 0) + 1
        return role

    def build_report(self) -> dict[str, object]:
        return {
            "total": self.get_total_users(),
            "active_count": len(self.get_active_users()),
            "role_count": self.count_by_role(),
            "frontend_names": [item.name for item in self.get_frontend_user()],
        }

    def deactivate_user(self, user_id: int) -> bool:
        for item in self.users:
            if item.user_id == user_id:
                item.active = False
                return True
        return False


print("=" * 30)
print("作业 3：定义报告方法")

# 任务：在 UserManager 里定义 build_report() -> dict[str, object]。
# 报告至少包含：
# - total
# - active_count
# - role_count
# - frontend_names
# 知识点：
# - 报告是把多个方法结果汇总成一个 dict。
# - 这是未来写 API 返回体时非常常见的结构。


print("=" * 30)
print("作业 4：创建样例数据并运行")

# 任务：创建至少 4 个用户，构造 UserManager，打印 build_report() 结果。
# 知识点：
# - 先准备输入数据，再调用类方法验证输出。
# - 这是最基础的“手工测试”方式。
ace = User(1, "Ace", "frontend")
lily = User(2, "Lily", "backend")
leo = User(3, "Leo", "frontend", False)
alice = User(4, "Alice", "qa")
print(UserManager([ace, lily, leo, alice]).build_report())
print("=" * 30)
print("作业 5：进阶（可选）")

# 任务：给 UserManager 增加 deactivate_user(user_id: int) -> bool。
# 找到对应用户就改成 active=False 并返回 True，否则返回 False。
# 知识点：
# - 这个方法体现“按条件更新对象状态”。
# - 返回 bool 能让调用方快速判断是否更新成功。
