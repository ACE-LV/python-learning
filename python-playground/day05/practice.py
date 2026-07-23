# 第五天练习题
# 主题：类、对象、dataclass、类型提示

# dataclass 适合做“轻量数据对象”，比手写 __init__ 更省代码。
from dataclasses import dataclass

print("=" * 30)
print("练习 1：定义 User 类")

# 任务：定义 User 类，要求：
# - __init__(user_id, name, role, active=True)
# - is_frontend()：role == "frontend" 返回 True，否则 False
# - to_dict()：返回用户字典
# 知识点：
# - __init__ 负责初始化对象属性。
# - self 代表当前对象，访问属性都写 self.xxx。
# - 方法返回布尔值时，常配合 -> bool 类型提示。

class UserClass:
    def __init__(self, user_id: int, name: str, role: str, active: bool = True):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.active = active

    def is_frontend(self) -> bool:
        return self.role == "frontend"

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.user_id,
            "name": self.name,
            "role": self.role,
            "active": self.active,
        }
@dataclass
class User:
    user_id: int
    name: str
    role: str
    active: bool = True


    def is_frontend(self) -> bool:
        return self.role == "frontend"

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.user_id,
            "name": self.name,
            "role": self.role,
            "active": self.active,
        }


print("=" * 30)
print("练习 2：创建对象并调用方法")

# 任务：创建 2 个 User 对象，打印 to_dict()，并打印 is_frontend() 结果。
# 知识点：
# - 类名(...) 是实例化。
# - 对象.方法() 是调用实例行为。
leo = UserClass(1, "Leo", "frontend")
ace = User(1, "Ace", "frontend")
lily = User(2, "Lily", "backend")
print(leo.to_dict())
print(leo.is_frontend())
print(ace)
print(ace.is_frontend())
print("=" * 30)
print("练习 3：定义 dataclass")

# 任务：定义 Course dataclass，字段：course_id, title, level, price。
# 创建一个 Course 对象并打印。
# 知识点：
# - @dataclass 会自动生成 __init__。
# - 字段后写类型，能增强可读性和 IDE 提示。

@dataclass
class Course:
    course_id: int
    title:str
    level:int
    price:str
print(Course(1, "Python 入门", "basic", '111'))
print("=" * 30)
print("练习 4：带类型提示的函数")

# 任务：定义函数 get_active_user_names(users) -> list[str]。
# 返回 active 为 True 的用户姓名列表。
# 知识点：
# - 参数类型：users: list[User]
# - 返回类型：list[str]
# - 这个函数适合用列表推导式实现。

def get_active_user_names(users: list[User]) -> list[str]:
    return [item.name for item in users if item.active]
print(get_active_user_names([User(1, "Ace", "frontend"), User(2, "Lily", "backend", False), User(3, "Tom", "qa")]))
print("=" * 30)
print("练习 5：组合输出")

# 任务：定义 build_user_dashboard(users) -> dict[str, object]。
# 返回内容包含：
# - total
# - active_count
# - frontend_names
# 知识点：
# - 组合输出就是把多个函数结果汇总成一个 dict。
# - 这是后续做接口返回、报表输出的基础模式。

def build_user_dashboard(users:list[User])-> dict[str,object]:
    return {
        'total':len(users),
        'active_count':len(get_active_user_names(users)),
        'frontend_names':[item.name for item in users if item.is_frontend()]
    }
[print(build_user_dashboard([User(1, "Ace", "frontend"), User(2, "Lily", "backend", False), User(3, "Tom", "qa")]))]