# Python 第三天：函数与模块

## 今日目标

今天学习 Python 中最常用的代码封装方式：函数。

你需要掌握：

1. 定义函数：`def`
2. 调用函数
3. 参数
4. 默认参数
5. 返回值：`return`
6. 函数里处理 `list` 和 `dict`
7. 模块导入：`import`

## 前端类比

| JavaScript / TypeScript | Python |
| --- | --- |
| `function getName() {}` | `def get_name():` |
| 箭头函数 | 普通函数 / `lambda` |
| `return value` | `return value` |
| `export / import` | `import / from ... import ...` |
| 工具函数文件 | Python 模块文件 |

## 今天重点

不要只会写一堆散代码，要开始学会封装：

```python
def get_frontend_users(users):
    return [item for item in users if item["role"] == "frontend"]
```

这就类似前端里的：

```js
function getFrontendUsers(users) {
  return users.filter(user => user.role === 'frontend')
}
```

## 学习顺序

1. 运行 `functions_demo.py`。
2. 阅读 `js-vs-python.md`。
3. 完成 `practice.py`。
4. 完成 `module_demo.py`，理解导入。
5. 完成 `homework.py`。
6. 写 `summary.md`。

## 今日验收标准

完成后你应该能：

- 把重复逻辑封装成函数。
- 知道什么时候用 `return`。
- 能给函数传入 `list` / `dict`。
- 能从另一个 `.py` 文件导入函数。
