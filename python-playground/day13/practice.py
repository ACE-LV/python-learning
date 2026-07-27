# 第十三天练习题
# 主题：Depends 与简单 token 鉴权

# 练习 1：把 API_TOKEN 改成从环境变量读取。
# 提示：使用 os.getenv("API_TOKEN", "dev-token")。

# 练习 2：新增公开接口 GET /public/version。

# 练习 3：新增受保护接口 DELETE /notes/{note_id}。
# 要求：缺 token 返回 401，找不到 note 返回 404。

# 练习 4：新增 require_admin_token。
# 要求：只有 Authorization: Bearer admin-token 可以访问 /admin/users。

# 练习 5：在 /docs 里分别测试有 token 和无 token 的请求。
