# 第三天：函数与返回值

print("第三天：函数与模块")
print("=" * 30)

# =========================
# 1. 最简单的函数
# =========================


def say_hello():
    print("Hello Python")


say_hello()

print("=" * 30)

# =========================
# 2. 带参数的函数
# =========================


def greet(name):
    print(f"你好，{name}")


greet("Ace")
greet("Lily")

print("=" * 30)

# =========================
# 3. 有返回值的函数
# =========================


def add(a, b):
    return a + b


result = add(10, 20)
print("计算结果：", result)

print("=" * 30)

# =========================
# 4. 默认参数
# =========================


def introduce(name, job="Frontend Developer"):
    return f"我是 {name}，职业是 {job}。"


print(introduce("Ace"))
print(introduce("Mia", "QA Engineer"))

print("=" * 30)

# =========================
# 5. 函数处理 dict
# =========================

user = {
    "name": "Ace",
    "role": "frontend",
    "city": "Shanghai",
}


def format_user_label(user_info):
    return f'{user_info["name"]} - {user_info["role"]}'


print(format_user_label(user))

print("=" * 30)

# =========================
# 6. 函数处理 list + dict
# =========================

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai"},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing"},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai"},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou"},
]


def get_frontend_users(user_list):
    return [item for item in user_list if item["role"] == "frontend"]


def get_user_names(user_list):
    return [item["name"] for item in user_list]


def count_by_role(user_list):
    role_count = {}

    for item in user_list:
        role = item["role"]
        role_count[role] = role_count.get(role, 0) + 1

    return role_count


frontend_users = get_frontend_users(users)
user_names = get_user_names(users)
role_count = count_by_role(users)

print("前端用户：", frontend_users)
print("用户姓名：", user_names)
print("角色统计：", role_count)

print("=" * 30)

# =========================
# 7. 函数可以复用
# =========================

more_users = [
    {"id": 5, "name": "Jack", "role": "frontend", "city": "Beijing"},
    {"id": 6, "name": "Nina", "role": "backend", "city": "Shanghai"},
]

print("新数据角色统计：", count_by_role(more_users))
