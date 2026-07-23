# 第一天练习题
# 请你把每一题补完整，然后运行本文件。

# 练习 1：定义变量
# 要求：定义你的姓名、职业、学习目标，然后打印出来。

name = "Ace"
job = "前端开发"
goal = "成为全栈开发者"

print("姓名：", name)
print("职业：", job)
print("学习目标：", goal)


# 练习 2：条件判断
# 要求：修改 score 的值，观察输出结果。

score = 44

if score >= 90:
    print("等级：A")
elif score >= 80:
    print("等级：B")
elif score >= 60:
    print("等级：C")
elif score >= 50:
    print("等级：D")
else:
    print("等级：E")


# 练习 3：循环
# 要求：打印 1 到 10。

for number in range(1, 11):
    print(number)

for i in range(0,100):
    print(i)
# 练习 4：字符串拼接
# 要求：用 f-string 输出一句完整介绍。

framework = "React / Vue"
language = "Python"
name = "Ace"
age = 18
title = "前端开发"
print(f"大家好，我是{name}，今年{age}岁，是一名前端开发工程师，熟悉{framework}，现在开始学习{language}。")

print(f"我熟悉 {framework}，现在开始学习 {language}。")


# 练习 5：BMI 计算
# 要求：修改 height 和 weight，计算自己的 BMI。

height = 1.80
weight = 80
bmi = weight / (height * height)

print(f"BMI：{bmi:.2f}")
