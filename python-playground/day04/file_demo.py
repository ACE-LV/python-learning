# 第四天示例
# 主题：文件、JSON、CSV、异常

import csv
import json
from pathlib import Path

# import csv：导入 Python 内置 CSV 模块，用来读取 .csv 表格文本。
# import json：导入 Python 内置 JSON 模块，用来做 JSON 字符串和 Python 数据互转。
# from pathlib import Path：只从 pathlib 模块里导入 Path 类，用来处理文件路径。

# Path(__file__)：当前这个 file_demo.py 文件的完整路径。
# .parent：取父目录，也就是 day04 目录。
# CURRENT_DIR：变量名，代表“当前 Python 文件所在目录”。
CURRENT_DIR = Path(__file__).parent

# 用 / 拼接路径，效果类似前端里的 path.join(...)。
# USERS_FILE：用户 JSON 示例文件路径。
# COURSES_FILE：课程 CSV 示例文件路径。
# OUTPUT_FILE：程序运行后要写出的 JSON 文件路径。
USERS_FILE = CURRENT_DIR / "sample_users.json"
COURSES_FILE = CURRENT_DIR / "sample_courses.csv"
OUTPUT_FILE = CURRENT_DIR / "output_users.json"

print("=" * 30)
print("1. 查看当前脚本目录")
print(CURRENT_DIR)

print("=" * 30)
print("2. 读取 JSON 文本")
# read_text 会把整个文件内容读成字符串。
# read_text 参数：
# - encoding="utf-8"：按 UTF-8 编码读取文件，避免中文乱码。
# json_text：变量名，代表“从 JSON 文件里读出来的原始字符串”。
json_text = USERS_FILE.read_text(encoding="utf-8")
print(json_text)

print("=" * 30)
print("3. JSON 字符串转 Python 数据")
# json.loads 类似 JavaScript 的 JSON.parse。
# loads 的 s 可以理解成 string，表示从 JSON 字符串加载数据。
# JSON 里的数组会变成 Python list，对象会变成 Python dict。
# users：变量名，代表用户列表。
# sample_users.json 里的字段含义：
# - id：用户 ID，唯一编号。
# - name：用户姓名。
# - role：用户角色，比如 frontend / backend / qa。
# - active：是否启用，JSON 里是 true / false，转成 Python 后是 True / False。
users = json.loads(json_text)
print(users)
# users[0]：取列表里的第 1 个用户。
# ["name"]：从这个用户 dict 里取 name 字段。
print("第一个用户：", users[0]["name"])

print("=" * 30)
print("4. 筛选 active 用户")
# 列表推导式：从 users 中挑出 active 为 True 的用户。
# 类似 JS：users.filter(user => user.active)
# user：循环变量，代表 users 列表里的每一个用户 dict。
# user["active"]：读取当前用户的 active 字段。
# active_users：筛选后的新列表，只包含启用用户。
active_users = [user for user in users if user["active"]]
print(active_users)

print("=" * 30)
print("5. 写入新的 JSON 文件")
# json.dumps 类似 JavaScript 的 JSON.stringify。
# dumps 的 s 可以理解成 string，表示把 Python 数据转成 JSON 字符串。
# json.dumps 参数：
# - active_users：要转换成 JSON 字符串的 Python 数据。
# - ensure_ascii=False：保留中文，不转成 \u4e2d 这种格式。
# - indent=2：用 2 个空格缩进，输出格式化后的 JSON，方便阅读。
# write_text 参数：
# - 第 1 个参数：要写入文件的字符串内容。
# - encoding="utf-8"：按 UTF-8 编码写入文件。
OUTPUT_FILE.write_text(
    json.dumps(active_users, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print("已写入：", OUTPUT_FILE)

print("=" * 30)
print("6. 读取 CSV 文件")
# with 会自动关闭文件，类似自动做 finally close。
# csv.DictReader 会把每一行 CSV 转成 dict。
# open 参数：
# - "r"：read，只读模式。
# - encoding="utf-8"：按 UTF-8 编码读取。
# - newline=""：读取 CSV 时推荐传这个，避免换行符被重复处理。
# file：变量名，代表打开后的文件对象。
# reader：CSV 读取器，会按表头生成 dict。
# courses：课程列表。
# sample_courses.csv 里的字段含义：
# - id：课程 ID。
# - title：课程标题。
# - level：课程难度，比如 basic / advanced。
# - price：课程价格。注意 CSV 读出来默认都是字符串。
with COURSES_FILE.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    print(f"reader", reader)
    courses = list(reader)
print(courses)

print("=" * 30)
print("7. 异常处理：读取不存在的文件")
# missing_file：故意构造一个不存在的文件路径，用来触发 FileNotFoundError。
missing_file = CURRENT_DIR / "missing.json"
try:
    # 这里故意读取一个不存在的文件，用来演示异常处理。
    missing_file.read_text(encoding="utf-8")
except FileNotFoundError:
    # 如果文件不存在，程序不会崩溃，而是走到这里。
    print("文件不存在：", missing_file)

print("=" * 30)
print("8. 封装函数：安全读取 JSON")


def read_json_file(file_path):
    # read_json_file：函数名，意思是“读取 JSON 文件”。
    # file_path：参数名，调用函数时传入的文件路径。
    # return：函数返回值。
    # - 成功时：返回 JSON 转换后的 Python 数据，通常是 list 或 dict。
    # - 失败时：返回 []，表示没有读到有效数据。
    # 把“读取文件 + 解析 JSON + 错误处理”封装成一个函数。
    # 以后读取任何 JSON 文件，都可以复用这个函数。
    try:
        # text：局部变量，只在这个函数内部使用，代表读取到的 JSON 字符串。
        text = file_path.read_text(encoding="utf-8")
        return json.loads(text)
    except FileNotFoundError:
        # 文件不存在时，返回空列表，调用方不用额外处理崩溃。
        print("文件不存在：", file_path)
        return []
    except json.JSONDecodeError:
        # 文件存在，但内容不是合法 JSON 时，走这里。
        print("JSON 格式错误：", file_path)
        return []


print(read_json_file(USERS_FILE))
