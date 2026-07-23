# 第二天练习题
# 主题：list / dict / set / tuple

# 练习 1：list 基础
# 要求：定义一个 frameworks 列表，包含你熟悉的前端框架。
# 然后新增一个 "Python"，最后打印整个列表。
# frameworks = ["react", "vue", "nodejs"]
# frameworks.append("Python")
# print(frameworks)


# frameworks = ["React", "Vue"]
# frameworks.append("Python")
# print("frameworks：", frameworks)


# 练习 2：遍历 list
# 要求：遍历 frameworks，每一项输出：我学过 xxx


# for item in frameworks:
#     print(f"我学过 {item}")


# for framework in frameworks:
#     print(f"我学过 {framework}")


# 练习 3：dict 基础
# 要求：定义一个 user 字典，包含 name、job、city 三个字段。
# 然后打印 name 和 job。
# user ={
#     'name': 'Ace',
#     "job": "Frontend Developer",
#     "city": "Shanghai"
# }
# print("姓名：", user["name"])
# print("职业：", user["job"])

# user = {
#     "name": "Ace",
#     "job": "Frontend Developer",
#     "city": "Shanghai",
# }

# print("姓名：", user["name"])
# print("职业：", user["job"])


# 练习 4：修改 dict
# 要求：给 user 增加一个字段 learning，值为 Python。

# user ={
#     'name':'Ace',
#     'job':'Frontend Developer',
#     'city':'Shanghai'
# }
# user['learning'] = 'Python'
# print("更新后的 user：", user)
# user.update({'life':'happy'})
# print("更新后的 user：", user)
# user["learning"] = "Python"
# print("更新后的 user：", user)


# 练习 5：list + dict
# 要求：从 users 里打印所有用户的 name。

# users = [
#     {"id": 1, "name": "Ace", "role": "frontend"},
#     {"id": 2, "name": "Lily", "role": "backend"},
#     {"id": 3, "name": "Tom", "role": "frontend"},
# ]

# for item in users:
#     print("用户", item["name"])

# for item in users:
#     print("用户：", item["name"])


# 练习 6：筛选数据
# 要求：只打印 role 是 frontend 的用户。

users = [
    {
        "name": "Ace",
        "role": "frontend",
    },
    {
        "name": "Lily",
        "role": "backend",
    },
    {
        "name": "Tom",
        "role": "frontend",
    },
]
# for item in users:
#     if item["role"] == "frontend":
#         print("前端用户：", item["name"])
print('前端用户', [item["name"] for item in users if item["role"] == "frontend"])
# for item in users:
#     if item["role"] == "frontend":
#         print("前端用户：", item["name"])


# 练习 7：set 去重
# 要求：对 cities 去重并打印。

# cities = ["Shanghai", "Beijing", "Shanghai", "Hangzhou", "Beijing"]
# unique_cities = set(cities)
# print("去重后的城市：", unique_cities)
