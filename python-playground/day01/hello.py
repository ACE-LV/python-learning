# 第一天：Python 入门
# 运行方式：在终端执行 python hello.py

# 1. 输出
print("Hello Python")
print("我是前端开发，今天开始学习 Python")

# 2. 变量
name = "Ace"
age = 18
is_frontend_developer = True

print("姓名：", name)
print("年龄：", age)
print("是否前端开发：", is_frontend_developer)

# 3. 字符串格式化
message = f"你好，我是 {name}，今年 {age} 岁。"
print(message)

# 4. 条件判断
score = 88

if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 5. 循环
for i in range(1, 6):
    print(f"这是第 {i} 次循环")

# 6. 简单计算
height = 1.75
weight = 68
bmi = weight / (height * height)
print(f"BMI 是：{bmi:.2f}")
