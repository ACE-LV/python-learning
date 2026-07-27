# 第十三天作业
# 主题：给接口加最小鉴权

# 作业要求：
# 1. 保留一个公开健康检查接口。
# 2. 新增 require_token 依赖函数。
# 3. 从 Authorization 请求头读取 Bearer token。
# 4. token 错误或缺失时返回 401。
# 5. 给 /me、/notes、/admin/users 加鉴权。
# 6. 在 summary.md 写清楚 401、403、404 的区别。
