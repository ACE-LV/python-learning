# 第二天补充：推导式练习
# 练习要求：每一题都自己写，不看答案。

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai", "years": 3},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing", "years": 5},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai", "years": 2},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou", "years": 4},
]

print("=" * 30)
print("1. 从 for 循环开始")


# 任务：用普通 for 循环生成所有用户姓名列表，并打印结果。
result = []
for item in users:
    result.append(item["name"])
print("A1", result)
print("=" * 30)
print("2. 改成 list 推导式")

# 任务：用 list 推导式生成所有用户姓名列表，并打印结果。
print("A2", [item["name"] for item in users])
print("=" * 30)
print("3. 加 if 过滤")

# 任务：用 list 推导式生成前端用户姓名列表，并打印结果。
print("A3", [item["name"] for item in users if item["role"] == "frontend"])
print("=" * 30)
print("4. 做数据转换")

# 任务：把每个用户转换成“姓名 - 角色”的字符串列表，并打印结果。
print("A4", [f"{item['name']}-{item['role']}" for item in users])
print("=" * 30)
print("5. 提取字段并去重")

# 任务：提取所有城市，再去重，并打印结果。
countries = [item["city"] for item in users]
unique_countries = set(countries)
print("A5", unique_countries)
print("=" * 30)
print("6. 生成新的 dict 列表")

# 任务：生成一个新的用户列表，每个用户只保留姓名和角色，并打印结果。
new_users = [{"name": item["name"], "role": item["role"]} for item in users]
print("A6", new_users)
print("=" * 30)
print("7. 拆分复杂逻辑")

# 任务：先筛选前端用户，再生成“姓名-城市”的字符串列表，并打印结果。
print(
    "A7",
    [f"{item['name']}-{item['city']}" for item in users if item["role"] == "frontend"],
)
