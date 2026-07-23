# 第四天：JS / TS 与 Python 文件处理对比

## 路径

JavaScript / TypeScript：

```ts
import path from 'node:path'

const filePath = path.join(process.cwd(), 'data', 'users.json')
```

Python：

```python
from pathlib import Path

file_path = Path.cwd() / "data" / "users.json"
```

## 读取文本

JavaScript / TypeScript：

```ts
import { readFileSync } from 'node:fs'

const text = readFileSync(filePath, 'utf-8')
```

Python：

```python
text = file_path.read_text(encoding="utf-8")
```

## JSON

JavaScript / TypeScript：

```ts
const users = JSON.parse(text)
const output = JSON.stringify(users, null, 2)
```

Python：

```python
import json

users = json.loads(text)
output = json.dumps(users, ensure_ascii=False, indent=2)
```

## 异常处理

JavaScript / TypeScript：

```ts
try {
  const users = JSON.parse(text)
} catch (error) {
  console.error(error)
}
```

Python：

```python
try:
    users = json.loads(text)
except json.JSONDecodeError as error:
    print(error)
```

## 记忆点

- Python 代码块靠缩进，不靠 `{}`。
- 文件路径优先用 `Path`，不要手写 `"a/b/c"` 拼接。
- 中文 JSON 输出时常用 `ensure_ascii=False`。
- 文件读写建议总是写 `encoding="utf-8"`。
