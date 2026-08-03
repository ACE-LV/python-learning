# 第十一天学习总结模板

## 今天学了什么

- 把单文件 API 拆成 `main.py`、`schemas.py`、`models.py`、`services.py` 分层结构。
- 用 `schemas.py` 管理请求/响应模型，保证接口边界清晰。
- 用 `services.py` 承载增删改查和报表逻辑，让路由层保持简洁。

## schema / model / service 分别负责什么

- `schema`：定义接口入参/出参结构（Pydantic 模型），负责类型与字段校验。
- `model`：定义内部数据对象（本练习用 dataclass），表示业务实体结构。
- `service`：封装业务逻辑（list/get/create/update/delete/report），不直接处理 HTTP 细节。

## 为什么 main.py 不适合放太多业务逻辑

- `main.py` 主要职责是路由映射和 HTTP 状态码转换。
- 如果把业务细节都堆在 `main.py`，文件会快速膨胀，难测试、难复用、难维护。
- 业务逻辑放在 `services.py` 后，可以独立测试并复用到其它入口。

## 今天完成的练习

- [x] 看懂 day11 文件结构
- [x] 启动 day11 服务
- [x] 新增一个 service 函数
- [x] 新增一个路由
- [x] 完成 homework

## 今天最容易混淆的点

- `schema` 和 `model` 容易混淆：`schema` 是 API 合同，`model` 是内部对象结构。
- `service` 返回 `None` 时不直接抛 HTTP 异常，由 `main.py` 统一转成 404 更符合分层职责。

## 明天想继续学什么

- 继续学习分页、搜索、筛选、排序的组合查询设计。
