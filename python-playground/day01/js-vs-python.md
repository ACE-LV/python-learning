# 第一天：JS / TS 对比 Python

## 变量

JavaScript：

```js
let name = 'Ace'
const age = 18
```

Python：

```python
name = 'Ace'
age = 18
```

Python 不需要 `let`、`const`，直接赋值。

## 输出

JavaScript：

```js
console.log('Hello')
```

Python：

```python
print('Hello')
```

## 条件判断

JavaScript：

```js
if (score >= 90) {
  console.log('优秀')
} else {
  console.log('继续努力')
}
```

Python：

```python
if score >= 90:
    print('优秀')
else:
    print('继续努力')
```

Python 使用冒号和缩进，不使用花括号。

## 循环

JavaScript：

```js
for (let i = 1; i <= 5; i++) {
  console.log(i)
}
```

Python：

```python
for i in range(1, 6):
    print(i)
```

注意：`range(1, 6)` 输出 1 到 5，不包含 6。
