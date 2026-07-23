# 第三天：JS / TS 对比 Python 函数

## 函数定义

JavaScript：

```js
function greet(name) {
  console.log(`你好，${name}`)
}
```

Python：

```python
def greet(name):
    print(f"你好，{name}")
```

## 返回值

JavaScript：

```js
function add(a, b) {
  return a + b
}
```

Python：

```python
def add(a, b):
    return a + b
```

## 默认参数

JavaScript：

```js
function introduce(name, job = 'Frontend Developer') {
  return `${name} - ${job}`
}
```

Python：

```python
def introduce(name, job="Frontend Developer"):
    return f"{name} - {job}"
```

## 处理数组对象

JavaScript：

```js
function getFrontendUsers(users) {
  return users.filter(user => user.role === 'frontend')
}
```

Python：

```python
def get_frontend_users(users):
    return [user for user in users if user["role"] == "frontend"]
```

## 导入工具函数

JavaScript：

```js
import { getFrontendUsers } from './utils'
```

Python：

```python
from utils import get_frontend_users
```

## 命名习惯

| JavaScript / TypeScript | Python |
| --- | --- |
| `getFrontendUsers` | `get_frontend_users` |
| `buildDashboard` | `build_dashboard` |
| camelCase | snake_case |

Python 函数名通常使用 `snake_case`。
