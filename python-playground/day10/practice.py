# 第十天练习题
# 主题：Pydantic 校验与 response_model

# 练习 1：给 UserCreate 新增 email 字段。
# 要求：先用普通 str，不要引入额外依赖。

# 练习 2：给 UserCreate 新增 level 字段。
# 要求：只能是 "junior"、"middle"、"senior"。

# 练习 3：实现 GET /users?role=frontend。
# 要求：role 可选，有值时过滤用户。

# 练习 4：新增 UserPrivate 模型。
# 要求：模拟内部字段 password_hash，但不要通过 response_model 返回。

# 练习 5：故意提交非法 age，观察 /docs 里的 422 响应。
