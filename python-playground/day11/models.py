from dataclasses import dataclass


@dataclass
class User:
    # models.py 放“内部数据结构”。
    # 这里的 User 不是 Pydantic 请求体，也不是数据库 ORM 模型；它只是当前示例里用于模拟业务数据的 Python 对象。
    # @dataclass 会自动帮我们生成 __init__，所以可以直接写 User(id=1, name="Alice", role="frontend")。
    id: int
    # 用户显示名称。Service 层会把它当作普通对象属性读取或修改。
    name: str
    # 用户角色。合法值由 schemas.py 里的 Role 负责校验，进入 service 后默认已经可信。
    role: str
    # 用户是否启用。这里有默认值 True，所以创建 User 时不传 active 也会默认启用。
    active: bool = True
