# 第四天作业
# 主题：文件处理小项目

import json
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
INPUT_FILE = CURRENT_DIR / "sample_users.json"
OUTPUT_FILE = CURRENT_DIR / "homework_user_report.json"

print("=" * 30)
print("作业 1：读取用户 JSON")

# 任务：读取 sample_users.json，转换成 users 列表。
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    users = json.load(f)
print("=" * 30)
print("作业 2：统计用户总数")


# 任务：定义 get_total_users(users)，返回用户总数，并打印结果。
def get_total_users(users):
    return len(users)


print("用户总数：", get_total_users(users))
print("=" * 30)
print("作业 3：统计 active 用户数")


# 任务：定义 count_active_users(users)，返回 active 为 True 的用户数量，并打印结果。
def count_active_users(users):
    return len([item for item in users if item["active"] == True])


print("active 用户数：", count_active_users(users))
print("=" * 30)
print("作业 4：按 role 统计")


# 任务：定义 count_by_role(users)，返回每种 role 有多少个用户，并打印结果。
def count_by_role(users):
    result = {}
    for item in users:
        role = item["role"]
        result[role] = result.get(role, 0) + 1

    return result


print("role 统计：", count_by_role(users))
print("=" * 30)
print("作业 5：生成用户报告")


# 任务：定义 build_user_report(users)，返回一个字典，并打印结果。
# 字典需要包含：用户总数、active 用户数、role 统计、所有 active 用户姓名。
def build_user_report(users):
    return {
        "total": get_total_users(users),
        "active": count_active_users(users),
        "role_count": count_by_role(users),
        "active_user_names": [item["name"] for item in users if item["active"] == True],
    }
print("用户报告：", build_user_report(users))

print("=" * 30)
print("作业 6：写入报告 JSON")

# 任务：把用户报告写入 homework_user_report.json。
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(json.dumps(build_user_report(users), ensure_ascii=False, indent=2))
print("已写入：", OUTPUT_FILE)
print("=" * 30)
print("作业 7：异常处理")

# 任务：封装 read_json_file(file_path)。
# 如果文件不存在，返回 []。
# 如果 JSON 格式错误，返回 []。
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在")
        return []
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 格式")
        return []