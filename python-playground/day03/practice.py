# 第三天练习题
# 主题：函数、参数、返回值、模块

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai", "years": 3},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing", "years": 5},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai", "years": 2},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou", "years": 4},
]

print("=" * 30)
print("练习 1：定义一个无参数函数")


# 任务：定义函数 print_title，打印“用户数据分析”。然后调用它。
def print_title():
    print("用户数据分析")


print_title()
print("=" * 30)
print("练习 2：定义带参数函数")


# 任务：定义函数 greet，接收 name，打印“你好，xxx”。然后调用它。
def greet(name):
    print(f"你好，{name}")


greet("Ace")
print("=" * 30)
print("练习 3：定义有返回值函数")


# 任务：定义函数 get_total_users，接收 user_list，返回用户总数。然后打印返回值。
def get_total_users(user_list):
    return len(user_list)


print("用户总数：", get_total_users(users))
print("=" * 30)
print("练习 4：封装获取姓名列表")


# 任务：定义函数 get_names，接收 user_list，返回所有用户姓名列表。
def get_name(user_list):
    return [item["name"] for item in user_list]


print("所有用户姓名：", get_name(users))
print("=" * 30)
print("练习 5：封装筛选 frontend 用户")


# 任务：定义函数 get_frontend_users，接收 user_list，返回 role 是 frontend 的用户列表。
def get_frontend_users(user_list):
    return [item["name"] for item in user_list if item["role"] == "frontend"]


print("前端用户姓名：", get_frontend_users(users))
print("=" * 30)
print("练习 6：封装字段统计")


# 任务：定义函数 count_by_role，接收 user_list，返回 role 统计结果。
def count_by_role(user_list):
    result = {}
    for item in user_list:
        role = item["role"]
        result[role] = result.get(role, 0) + 1
    return result    


print("角色统计结果：", count_by_role(users))
print("=" * 30)
print("练习 7：封装 dashboard")


# 任务：定义函数 build_dashboard，返回一个字典，包含用户总数、角色统计、前端用户姓名列表。
def build_dashboard():
    result = {}
    result["total_count"] = get_total_users(users)
    result["role_count"] = count_by_role(users)
    result["frontend_users"] = get_frontend_users(users)
    return result


print("用户数据分析仪表盘：", build_dashboard())
