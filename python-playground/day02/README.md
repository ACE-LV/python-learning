# Python 第二天：数据结构

## 今日目标

今天学 Python 里最常用的 4 种数据结构：

1. `list`：列表，类似 JavaScript 的数组。
2. `dict`：字典，类似 JavaScript 的对象。
3. `set`：集合，类似 JavaScript 的 Set，用来去重。
4. `tuple`：元组，类似不能随便改的数组。

## 前端类比

| JavaScript / TypeScript | Python | 用途 |
| --- | --- | --- |
| `Array` | `list` | 存一组有顺序的数据 |
| `Object` / `Record` | `dict` | 存键值对 |
| `Set` | `set` | 去重、集合判断 |
| readonly array | `tuple` | 固定数据 |

## 学习顺序

1. 先运行 `collections_demo.py`。
2. 看 `js-vs-python.md`，用前端知识类比理解。
3. 修改并运行 `practice.py`。
4. 独立完成 `homework.py`。
5. 最后写 `summary.md`。

补充训练：

- `comprehension_guide.py`：推导式训练。
- `dict_counting_drill.py`：字典统计训练。

## 今天重点记住

### list

```python
users = ["Ace", "Lily", "Tom"]
print(users[0])
users.append("Mia")
```

### dict

```python
user = {
    "name": "Ace",
    "job": "Frontend Developer"
}
print(user["name"])
```

### set

```python
roles = {"admin", "user", "user"}
print(roles)
```

### tuple

```python
point = (10, 20)
print(point[0])
```

## 今日小项目

做一个“接口返回数据统计器”：

- 给定一组用户数据。
- 统计用户总数。
- 提取所有城市。
- 按角色统计数量。
- 找出前端开发者。

这个练习很贴近前端日常处理接口响应数据。
