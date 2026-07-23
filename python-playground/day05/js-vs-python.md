# 第五天：JS / TS 与 Python 面向对象对比

## 类定义

JavaScript / TypeScript：

```ts
class User {
  constructor(public name: string, public role: string) {}

  isFrontend(): boolean {
    return this.role === 'frontend'
  }
}
```

Python：

```python
class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def is_frontend(self) -> bool:
        return self.role == "frontend"
```

## 数据类

TypeScript 常用 interface/type 描述数据结构；
Python 常用 `dataclass`。

```python
from dataclasses import dataclass

@dataclass
class Course:
    id: int
    title: str
    level: str
```

## 记忆点

- `self` 相当于 JS 里的 `this`。
- `__init__` 相当于 constructor。
- `dataclass` 适合“主要存数据”的类。
- 类型提示不强制运行时检查，但能提升可读性和 IDE 提示。
