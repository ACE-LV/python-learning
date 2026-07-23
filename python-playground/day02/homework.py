# 第二天作业
# 主题：list / dict / set / tuple

# 作业 1：前端技能列表
# 定义 skills 列表，至少包含 4 个技能，例如 React、Vue、TypeScript、CSS。
# 要求：
# 1. 打印第一个技能。
# 2. 添加一个新技能 Python。
# 3. 遍历并打印所有技能。
skills = ["React", "Vue", "TypeScript", "CSS"]
print("第一个技能：", skills[0])
skills.append("Python")
print("更新后的技能列表：", skills)

# 作业 2：个人信息字典
# 定义 profile 字典，包含：name、job、years、city、target。
# 要求：
# 1. 打印 name 和 target。
# 2. 把 years 加 1。
# 3. 新增字段 learning_day，值为 2。
# 4. 打印完整 profile。

profile = {
    "name": "Ace",
    "job": "Frontend Developer",
    "years": 3,
    "city": "Shanghai",
    "target": "Python",
}
print("姓名", profile["name"])
print("目标", profile["target"])
profile["years"] += 1
profile["learning_day"] = 2
print("更新后的 profile：", profile)

# 作业 3：接口用户数据处理
# 给定 users，完成下面任务。

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai"},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing"},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai"},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou"},
    {"id": 5, "name": "Jack", "role": "frontend", "city": "Beijing"},
]

# 要求 1：打印用户总数。
print("用户总数：", len(users))

# 要求 2：打印所有用户姓名。

print("所有用户姓名", [item["name"] for item in users])
# 要求 3：只打印 frontend 用户姓名。

print("前端用户姓名", [item["name"] for item in users if item["role"] == "frontend"])
# 要求 4：统计 frontend 用户数量。


# 要求 5：提取所有城市并去重。

cities = [item["city"] for item in users]
unique_cities = set(cities)
print("去重后的城市", unique_cities)
# 作业 4：角色统计
# 要求：统计每种 role 有多少人。
# 期望结果类似：
# {'frontend': 3, 'backend': 1, 'qa': 1}

dict = {}
for item in users:
    dict[item["role"]] = dict.get(item["role"], 0) + 1
print("角色统计结果", dict)

# 作业 5：切片练习
# 给定 numbers，打印：
# 1. 前 3 个数字。
# 2. 后 3 个数字。
# 3. 第 2 到第 5 个数字。

numbers = [10, 20, 30, 40, 50, 60, 70]
for item in numbers[:3]:
    print("前 3 个数字：", item)
for item in numbers[-3:]:
    print("后 3 个数字：", item)
for item in numbers[1:5]:
    print("第 2 到第 5 个数字：", item)
print("前3个数字", numbers[:3])
print("前3个数字", numbers[-3:])
print("前3个数字", numbers[1:5])
