# 第十三天学习总结模板

## 今天学了什么

- `Depends` 可以在接口执行前先运行鉴权函数。
- `Header` 可以从请求头里读取 `Authorization`。
- token 不合法时可以用 `HTTPException` 主动返回错误状态码。

## Depends 的作用

- 把通用逻辑抽成依赖函数，比如 token 校验。
- 哪个接口参数写了 `Depends(require_token)`，FastAPI 就会先执行 `require_token`。
- 依赖函数抛异常时，接口函数体不会继续执行。

## 401 / 403 / 404 的区别

- `401`：没有登录，或者 token 缺失/错误。
- `403`：已经通过身份校验，但没有权限访问这个资源。
- `404`：请求的资源不存在，比如指定 id 的 note 找不到。

## 今天完成的练习

- [x] 启动 day13 服务
- [x] 测试公开接口
- [x] 测试无 token 的受保护接口
- [x] 测试正确 token
- [x] 完成 homework

## 今天最容易混淆的点

- `Depends(require_token)` 的参数值来自依赖函数返回值，不是前端直接传的 query 参数。
- `session.get(Model, id)` 适合按主键查一条；复杂条件继续用 `select(...).where(...)`。
- `commit` 是写入数据库，`refresh` 是再从数据库读回最新值。

## 明天想继续学什么

- 继续练习把鉴权逻辑拆到独立文件，并区分普通用户和管理员权限。
