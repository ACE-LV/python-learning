# 第八天练习题
# 主题：FastAPI + SQLite

# 目标：在 day08/main.py 的基础上做二次练习。

# 练习 1：实现 DELETE /users/{user_id}
# 要求：删除成功返回 {"ok": True}；找不到返回 404。

# 练习 2：实现 PATCH /users/{user_id}/deactivate
# 要求：把 active 设为 0，返回更新后的用户。

# 练习 3：实现 GET /users?role=frontend
# 要求：支持可选 query 参数 role 做过滤。

# 练习 4：实现 POST /seed
# 要求：插入 3 条测试数据，返回新增数量。

# 练习 5（可选）：
# 新增字段 created_at，并在插入时写入当前时间。
