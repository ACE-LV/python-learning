# Python 第五天：类、对象、dataclass、类型提示

## 今日目标

今天你会从“写函数”进阶到“组织数据和行为”，开始理解面向对象和类型提示。

你需要掌握：

1. 定义类和创建对象。
2. 使用 `__init__` 初始化实例属性。
3. 写实例方法。
4. 使用 `@dataclass` 简化数据类。
5. 添加常见类型提示（`str`、`int`、`list[str]`、`dict[str, int]`）。

## 前端类比

| JavaScript / TypeScript | Python |
| --- | --- |
| `class User {}` | `class User:` |
| `constructor(...)` | `def __init__(...)` |
| `this.name` | `self.name` |
| `interface` / `type` | `dataclass` + 类型提示 |

## 今日重点

先掌握类的最小结构：

```python
class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def is_frontend(self) -> bool:
        return self.role == "frontend"
```

## 学习顺序

1. 运行 `class_demo.py`。
2. 阅读 `js-vs-python.md`。
3. 完成 `practice.py`。
4. 完成 `homework.py`。
5. 写 `summary.md`。

## 今日验收标准

完成后你应该能：

- 用类封装“数据 + 行为”。
- 理解 `self`、`__init__`、实例方法。
- 用 `@dataclass` 定义轻量数据模型。
- 给函数和方法补上基础类型提示。
