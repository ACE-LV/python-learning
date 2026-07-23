# 第四天练习题
# 主题：文件、JSON、CSV、异常

import csv
import json
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
USERS_FILE = CURRENT_DIR / "sample_users.json"
COURSES_FILE = CURRENT_DIR / "sample_courses.csv"
OUTPUT_FILE = CURRENT_DIR / "practice_active_frontend_users.json"

print("=" * 30)
print("练习 1：读取 JSON 文件")

# 任务：读取 sample_users.json，并把内容转换成 users 列表。
with open(USERS_FILE, "r", encoding="utf-8") as f:
    users = json.load(f)
# print(users)
print("=" * 30)
print("练习 2：打印所有用户姓名")

# 任务：遍历 users，打印每个用户的 name。
# print([item['name'] for item in users])
print("=" * 30)
print("练习 3：筛选 active 用户")

# 任务：用列表推导式筛选 active 为 True 的用户。
# print([item for item in users if item['active'] == True])
print("=" * 30)
print("练习 4：筛选 active frontend 用户")

# 任务：筛选 role 是 frontend 且 active 为 True 的用户。

print("=" * 30)
print("练习 5：写入 JSON 文件")

# 任务：把 active frontend 用户写入 practice_active_frontend_users.json。
# 提示：使用 json.dumps(..., ensure_ascii=False, indent=2)。
user = [item for item in users if item["active"] == True and item["role"] == "frontend"]
result = json.dumps(user, ensure_ascii=False, indent=2)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(result)
# print(OUTPUT_FILE, "写入成功")

print("=" * 30)
print("练习 6：读取 CSV 文件")

# 任务：读取 sample_courses.csv，转换成 courses 列表，并打印。
with open(COURSES_FILE,'r',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print(reader)
    courses = list(reader)
    print(courses)
print(courses)
print("=" * 30)
print("练习 7：封装安全读取 JSON 函数")

# 任务：定义 read_json_file(file_path)，正常时返回 JSON 数据。
# 如果文件不存在，打印提示并返回 []。
# 如果 JSON 格式错误，打印提示并返回 []。

def read_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在")
        return []
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 格式")
        return []