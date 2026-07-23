# 第二天：JS / TS 对比 Python 数据结构

## Array vs list

JavaScript：

```js
const names = ['Ace', 'Lily', 'Tom']
names.push('Mia')
console.log(names[0])
```

Python：

```python
names = ['Ace', 'Lily', 'Tom']
names.append('Mia')
print(names[0])
```

区别：

- JS 用 `push()`。
- Python 用 `append()`。

## Object vs dict

JavaScript：

```js
const user = {
  name: 'Ace',
  job: 'Frontend Developer'
}
console.log(user.name)
console.log(user['job'])
```

Python：

```python
user = {
    'name': 'Ace',
    'job': 'Frontend Developer'
}
print(user['name'])
print(user['job'])
```

Python 字典最常用 `user['name']` 访问字段。

## Array of Object vs list of dict

JavaScript：

```js
const users = [
  { id: 1, name: 'Ace', role: 'frontend' },
  { id: 2, name: 'Lily', role: 'backend' }
]
```

Python：

```python
users = [
    {'id': 1, 'name': 'Ace', 'role': 'frontend'},
    {'id': 2, 'name': 'Lily', 'role': 'backend'},
]
```

## filter 对比

JavaScript：

```js
const frontendUsers = users.filter(user => user.role === 'frontend')
```

Python 入门写法：

```python
frontend_users = []

for user in users:
    if user['role'] == 'frontend':
        frontend_users.append(user)
```

Python 推导式写法：

```python
frontend_users = [user for user in users if user['role'] == 'frontend']
```

## map 对比

JavaScript：

```js
const names = users.map(user => user.name)
```

Python 入门写法：

```python
names = []

for user in users:
    names.append(user['name'])
```

Python 推导式写法：

```python
names = [user['name'] for user in users]
```

## Set 去重

JavaScript：

```js
const cities = ['Shanghai', 'Beijing', 'Shanghai']
const uniqueCities = new Set(cities)
```

Python：

```python
cities = ['Shanghai', 'Beijing', 'Shanghai']
unique_cities = set(cities)
```

## 重点区别

| 概念 | JavaScript | Python |
| --- | --- | --- |
| 数组 | `Array` | `list` |
| 对象 | `Object` | `dict` |
| 去重集合 | `Set` | `set` |
| 添加数组项 | `push()` | `append()` |
| 长度 | `array.length` | `len(list)` |
| 包含判断 | `includes()` | `in` |
