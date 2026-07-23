# 作业 5 讲解：前端构建日志统计

# 假设这是一次前端项目构建后的日志。
# 类似你平时看到的 npm run build / pnpm build 输出。
log = "build success, 2 warning, 0 error"

print("原始日志：")
print(log)
print("-" * 30)

# =========================
# 版本 1：入门版
# =========================
# 目标：只判断某个关键词有没有出现在字符串里。
# 这是第一天要掌握的重点：if + in。

if "error" in log:
    print("日志里出现了 error 这个词")
else:
    print("日志里没有 error 这个词")

if "warning" in log:
    print("日志里出现了 warning 这个词")
else:
    print("日志里没有 warning 这个词")

if "success" in log:
    print("日志里出现了 success 这个词")
else:
    print("日志里没有 success 这个词")

print("-" * 30)

# 注意：
# 上面的判断只看“单词是否出现”。
# log 里面虽然是 0 error，但 error 这个单词确实出现了。
# 所以入门版会说：发现 error。


# =========================
# 版本 2：计数关键词出现次数
# =========================
# 目标：统计 error / warning / success 这些单词各出现了几次。
# 这里统计的是“单词出现次数”，不是日志里的数字。

error_word_count = log.count("error")
warning_word_count = log.count("warning")
success_word_count = log.count("success")

print(f"error 单词出现次数：{error_word_count}")
print(f"warning 单词出现次数：{warning_word_count}")
print(f"success 单词出现次数：{success_word_count}")

print("-" * 30)


# =========================
# 版本 3：进阶版，读取日志里的数字
# =========================
# 目标：从 '2 warning'、'0 error' 里取出真实数量。
# 这个还不是第一天必须掌握的内容，先看懂即可。

parts = log.split(", ")
# parts 会变成：
# ['build success', '2 warning', '0 error']

warning_count = 0
error_count = 0
success = False

for part in parts:
    if "success" in part:
        success = True

    if "warning" in part:
        warning_count = int(part.split(" ")[0])

    if "error" in part:
        error_count = int(part.split(" ")[0])

print(f"是否构建成功：{success}")
print(f"真实 warning 数量：{warning_count}")
print(f"真实 error 数量：{error_count}")

# 前端类比：
# JavaScript 里可以写：
# log.includes('error')
# Python 里写：
# 'error' in log
