# 第三天：模块导入
# 这个文件演示如何从 utils.py 导入函数。

from utils import build_dashboard, count_by_field, get_frontend_users, get_user_names

users = [
    {"id": 1, "name": "Ace", "role": "frontend", "city": "Shanghai"},
    {"id": 2, "name": "Lily", "role": "backend", "city": "Beijing"},
    {"id": 3, "name": "Tom", "role": "frontend", "city": "Shanghai"},
    {"id": 4, "name": "Mia", "role": "qa", "city": "Hangzhou"},
]

print("前端用户：", get_frontend_users(users))
print("用户姓名：", get_user_names(users))
print("角色统计：", count_by_field(users, "role"))
print("城市统计：", count_by_field(users, "city"))
print("看板数据：", build_dashboard(users))
