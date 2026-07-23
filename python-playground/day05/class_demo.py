# 第五天示例
# 主题：类、对象、dataclass、类型提示

# dataclass 用于“主要存数据”的类，能自动生成 __init__、__repr__ 等常用方法。
from dataclasses import dataclass


class User:
    # __init__ 在创建对象时自动调用，负责给实例绑定初始属性。
    def __init__(self, user_id: int, name: str, role: str, active: bool = True):
        # self 代表“当前对象本身”，类似前端里的 this。
        self.user_id = user_id
        self.name = name
        self.role = role
        self.active = active

    # 实例方法：描述“这个对象会做什么”。
    def is_frontend(self) -> bool:
        return self.role == "frontend"

    # 修改对象内部状态的常见写法。
    def deactivate(self) -> None:
        self.active = False

    # 把对象转换成字典，方便打印、序列化或接口返回。
    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.user_id,
            "name": self.name,
            "role": self.role, 
            "active": self.active,
        }


@dataclass
class Course:
    # dataclass 里通常只放字段定义，适合“数据模型”。
    course_id: int
    title: str
    level: str
    price: int


# 类型提示：参数 users 是 User 列表，返回值是字符串列表。
def get_active_user_names(users: list[User]) -> list[str]:
    return [user.name for user in users if user.active]


print("=" * 30)
print("1. 创建对象")
# 通过类名(...) 来创建对象，也叫“实例化”。
ace = User(1, "Ace", "frontend")
lily = User(2, "Lily", "backend")
print(ace.to_dict())
print(lily.to_dict())

print("=" * 30)
print("2. 调用实例方法")
# 对象.方法()：调用该对象的行为。
print("Ace 是否前端：", ace.is_frontend())
print("Lily 是否前端：", lily.is_frontend())

print("=" * 30)
print("3. 修改对象状态")
# 调用方法后，lily.active 会从 True 变成 False。
lily.deactivate()
print(lily.to_dict())

print("=" * 30)
print("4. dataclass 示例")
# dataclass 默认打印效果清晰，便于调试。
python_course = Course(1, "Python Basic", "basic", 99)
print(python_course)

print("=" * 30)
print("5. 列表 + 类型提示函数")
# 把对象放进列表，再交给函数处理，是业务代码里很常见的模式。
users = [ace, lily]
print("active 用户姓名：", get_active_user_names(users))
