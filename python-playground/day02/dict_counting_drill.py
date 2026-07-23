# 第二天补充：dict 统计训练
# 练习要求：自己完成每一题，不看答案，不放代码提示。

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai", "years": 3},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing", "years": 5},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai", "years": 2},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou", "years": 4},
    {"id": 5, "name": "Jack", "role": "frontend", "city": "Beijing", "years": 1},
    {"id": 6, "name": "Nina", "role": "backend", "city": "Shanghai", "years": 6},
]

print("=" * 30)
print("1. 统计用户总数")

# 任务：统计 users 里一共有多少个用户，并打印结果。
print("用户总数：", len(users))
print("=" * 30)
print("2. 统计 frontend 用户数量")

# 任务：统计 role 是 frontend 的用户数量，并打印结果。
print(
    "前端用户总数：",
    len([item["name"] for item in users if item["role"] == "frontend"]),
)
print("=" * 30)
print("3. 按 role 统计人数")

# 任务：统计每种 role 分别有多少人，并打印结果。
role_count = {}
for item in users:
    role_count[item["role"]] = role_count.get(item["role"], 0) + 1
print("角色统计结果", role_count)
print("=" * 30)
print("4. 按 city 统计人数")

# 任务：统计每个 city 分别有多少人，并打印结果。
cities_count = {}
for item in users:
    cities_count[item["city"]] = cities_count.get(item["city"], 0) + 1
print("城市统计结果", cities_count)

print("=" * 30)
print("5. 找出工作年限大于等于 3 年的用户")
print("工作年限大约3的用户是", [item["name"] for item in users if item["years"] >= 3])
# 任务：找出 years 大于等于 3 的用户姓名，并打印结果。

print("=" * 30)
print("6. 生成用户看板数据")

# 任务：生成一个 dashboard 字典，并打印结果。
# dashboard 需要包含：用户总数、角色统计、城市统计、前端用户姓名列表。
dashboard = {
    "total_users": len(users),
    "role_count": role_count,
    "cities_count": cities_count,
    "frontend_users": [item["name"] for item in users if item["role"] == "frontend"],
}

print("用户看板数据：", dashboard)
