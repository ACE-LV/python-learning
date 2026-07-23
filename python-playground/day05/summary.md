# 第五天学习总结模板

## 今天学了什么

- 
- class
- class、对象、self 的关系
- __init__ 和实例方法的职责
- dataclass 的简化写法和使用场景
- 类型提示（list[User]、dict[str, object]）
- class 类模型
- class 是模板，对象是实例。
- self 代表当前对象本身，访问属性要写 self.xxx。
- 
- __init__ 在实例化时自动调用，负责初始化属性。
- 实例方法用于描述对象行为，需要通过 对象.方法() 调用。

## `__init__` 和实例方法的区别

- 当类主要用于存储字段数据时用 dataclass。
- 想减少样板代码（__init__、__repr__）时优先使用。

## `dataclass` 什么时候用

## 今天完成的练习

- [X] 运行 `class_demo.py`
- [X] 阅读 `js-vs-python.md`
- [X] 完成 `practice.py`
- [X] 完成 `homework.py`
- [X] 完成 `homework.py`

- 方法是否在 class 缩进内（否则不是类方法）。
- dataclass 和普通 class 的适用边界。

## 今天最容易混淆的点

- HTTP 请求与 FastAPI 基础。

## 明天想继续学什么
