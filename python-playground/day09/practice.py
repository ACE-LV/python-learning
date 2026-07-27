# 第九天练习题
# 主题：SQLAlchemy ORM

# 练习 1：在 User 模型上新增 email 字段。
# 提示：新增 mapped_column(String(120), nullable=True)。

# 练习 2：修改 POST /users，让它能保存 email。

# 练习 3：实现 DELETE /users/{user_id}。
# 要求：删除成功返回 {"ok": True}；找不到返回 404。

# 练习 4：实现 GET /users?role=frontend。
# 要求：role 是可选 query 参数，有值时按角色过滤。

# 练习 5：实现 PATCH /users/{user_id}/deactivate。
# 要求：把 active 改成 False，并返回更新后的用户。
