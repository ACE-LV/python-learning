# 第二天：Python 数据结构
# 主题：list / dict / set / tuple

print("第二天：数据结构")
print("=" * 30)

# =========================
# 1. list：列表
# =========================
# 类似 JavaScript 的 Array

names = ["Ace", "Lily", "Tom"]

print("原始 names：", names)
print("第一个人：", names[0])
print("最后一个人：", names[-1])

names.append("Mia")
print("append 后：", names)

names.remove("Tom")
print("remove 后：", names)

print("遍历 names：")
for name in names:
    print("-", name)

print("=" * 30)

# =========================
# 2. dict：字典
# =========================
# 类似 JavaScript 的 Object / Record

user = {
    "name": "Ace",
    "job": "Frontend Developer",
    "years": 3,
    "city": "Shanghai",
}

print("用户信息：", user)
print("姓名：", user["name"])
print("职业：", user["job"])

# 修改字典里的值
user["years"] = 4
print("修改工作年限后：", user)

# 新增字段
user["learning"] = "Python"
print("新增学习目标后：", user)

print("遍历 user：")
for key, value in user.items():
    print(f"{key}: {value}")

print("=" * 30)

# =========================
# 3. list + dict：接口数据
# =========================
# 前端最常见：接口返回数组，数组里每一项是对象。
# Python 里就是：list 里面放 dict。

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai"},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing"},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai"},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou"},
]

print("用户总数：", len(users))

print("所有用户名：")
for item in users:
    print(item["name"])

print("前端开发者：")
for item in users:
    if item["role"] == "frontend":
        print(item["name"])

print("=" * 30)

# =========================
# 4. set：集合
# =========================
# 类似 JavaScript 的 Set，常用于去重。

cities = ["Shanghai", "Beijing", "Shanghai", "Hangzhou"]
unique_cities = set(cities)

print("原始城市列表：", cities)
print("去重后的城市：", unique_cities)

# 从接口数据里提取城市并去重
user_cities = set()
for item in users:
    user_cities.add(item["city"])

print("用户所在城市：", user_cities)

print("=" * 30)

# =========================
# 5. tuple：元组
# =========================
# 类似一个固定的数组，不建议修改。

position = (120, 80)
print("坐标：", position)
print("x：", position[0])
print("y：", position[1])

print("=" * 30)

# =========================
# 6. 切片
# =========================
# 切片可以取 list 的一部分。

numbers = [1, 2, 3, 4, 5, 6]
print("numbers：", numbers)
print("前 3 个：", numbers[:3])
print("从第 3 个开始：", numbers[2:])
print("中间一段：", numbers[1:4])

print("=" * 30)

# =========================
# 7. 简单推导式
# =========================
# 类似 JavaScript 的 map/filter，但写法更短。

frontend_names = [item["name"] for item in users if item["role"] == "frontend"]
print("前端开发者姓名列表：", frontend_names)
