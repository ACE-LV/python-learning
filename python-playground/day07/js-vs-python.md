# 第七天：前端测试/日志 与 Python 对比

## 测试工具

- 前端常见：Jest / Vitest
- Python 常见：pytest

## 断言

前端：

```ts
expect(sum(1, 2)).toBe(3)
```

Python：

```python
def test_sum():
    assert add(1, 2) == 3
```

## 日志

前端：

```ts
console.log('start')
console.error('failed')
```

Python：

```python
import logging

logging.info('start')
logging.error('failed')
```

## 记忆点

- pytest 函数名通常以 `test_` 开头。
- `assert` 是 Python 测试里的核心语句。
- 生产代码不要只靠 `print`，尽量用 logging。
