# 第一天作业
# 要求：独立完成，不要直接复制 hello.py。

# 作业 1：个人介绍
# 定义 name、job、years、target 四个变量，并输出一句完整介绍。
# name = 'Ace'
# job = '前端开发'
# years = 3
# target = 'Python 开发'
# print(f"大家好，我是 {name}，我是一名 {job}，有 {years} 年的工作经验。现在我想转行成为一名 {target}。")

# 作业 2：分数评级
# 定义 score：
# >= 90 输出 A
# >= 80 输出 B
# >= 60 输出 C
# < 60 输出 D

# score = 85
# if score >= 90:
#     print("A")
# elif score >= 80:
#     print("B")
# elif score >= 60:
#     print("C")
# else:
#     print("D")


# 作业 3：打印 1 到 20 中的偶数
# 提示：可以使用 if number % 2 == 0
# for num in range(1, 21):
#     if num % 2 == 0:
#         print(num)

# 作业 4：BMI 计算器
# 定义 height 和 weight，计算 BMI。
# BMI = weight / (height * height)
# height = 1.80
# weight = 80
# BMI = weight / (height * height)
# print(f"BMI 是：{BMI:.2f}")


# 作业 5：前端构建日志统计
# 给定一段日志字符串，统计 error、warning、success 是否出现。

log = "build success, 2 warning, 0 error"

# 你可以先用下面这种方式判断：
# if "error" in log:
#     print("发现 error")
errorNum = 0
warningNum = 0
successNum = 0
if "error" in log:
    print("发现 error")
    errorNum = int(errorNum + 1)
if "warning" in log:
    print("发现 warning")
    warningNum = int(warningNum + 1)
if "success" in log:
    print("发现 success")
    successNum = int(successNum + 1)
print(f"error 数量：{errorNum}")
print(f"warning 数量：{warningNum}")
print(f"success 数量：{successNum}")
