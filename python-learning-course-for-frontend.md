# Python 学习课程：前端开发者版

适合对象：已有 JavaScript / TypeScript / React / Vue 基础，希望系统学习 Python，并能用于脚本自动化、接口开发、数据处理、AI 工具链或全栈开发。

建议节奏：每天 60-90 分钟，每周 5 天，持续 8 周。

## 学习目标

完成课程后，你应该能够：

- 熟练使用 Python 基础语法、函数、模块、包和异常处理。
- 理解 Python 与 JavaScript / TypeScript 的核心差异。
- 使用 `venv`、`pip`、`requirements.txt` 管理项目依赖。
- 编写命令行脚本，自动处理文件、JSON、Excel、接口数据。
- 使用 `FastAPI` 编写 REST API，并理解前后端联调流程。
- 使用 `pytest` 编写基础单元测试。
- 具备继续学习数据分析、AI、自动化测试或后端开发的基础。

## 前置准备

### 必备工具

- Python 3.11 或 3.12
- VS Code Python 插件
- Git
- Postman / Apifox / Thunder Client 任意一个接口调试工具

### 建议学习方式

- 不要只看视频，每天必须写代码。
- 每个知识点都用“JS / TS 对比 Python”的方式理解。
- 每周至少完成一个小项目。
- 学完基础后尽快进入接口开发或自动化脚本，不要长期停留在语法阶段。

## 第 1 周：Python 基础语法

目标：能写简单脚本，理解 Python 代码结构。

### 学习内容

- 安装 Python，配置 VS Code。
- `print()`、变量、注释、缩进。
- 基础类型：`int`、`float`、`str`、`bool`、`None`。
- 运算符、字符串格式化。
- 条件判断：`if` / `elif` / `else`。
- 循环：`for` / `while`。
- 基础输入输出。

### 前端类比

| JavaScript / TypeScript  | Python           |
| ------------------------ | ---------------- |
| `null` / `undefined` | `None`         |
| `let name = 'Tom'`     | `name = 'Tom'` |
| `{}` 代码块            | 缩进代码块       |
| `console.log()`        | `print()`      |
| `===`                  | `==`           |

### 练习

- 写一个 BMI 计算器。
- 写一个根据分数判断等级的脚本。
- 写一个九九乘法表。
- 写一个简单的命令行菜单。

### 小项目

实现一个“前端构建日志分析器”：输入一段构建日志文本，统计 `error`、`warning`、`success` 出现次数。

## 第 2 周：数据结构

目标：熟悉 Python 常用容器，能处理列表、字典和集合数据。

### 学习内容

- 列表：`list`
- 元组：`tuple`
- 字典：`dict`
- 集合：`set`
- 切片、遍历、推导式。
- 排序、过滤、映射。

### 前端类比

| JavaScript / TypeScript  | Python                           |
| ------------------------ | -------------------------------- |
| `Array`                | `list`                         |
| `Object` / `Record`  | `dict`                         |
| `Set`                  | `set`                          |
| `map()` / `filter()` | 推导式 /`map()` / `filter()` |
| 解构                     | 解包                             |

### 练习

- 将接口返回的用户列表按年龄排序。
- 从数组中去重。
- 统计字符串中每个字符出现次数。
- 将多个接口响应合并成一个字典。

### 小项目

实现一个“Mock 数据清洗工具”：读取一组用户 JSON 数据，过滤无效数据，按字段分组统计。

## 第 3 周：函数、模块与包

目标：写出可复用、可维护的 Python 代码。

### 学习内容

- 函数定义：`def`
- 参数、默认参数、关键字参数。
- 返回值。
- 作用域。
- Lambda。
- 模块导入：`import`、`from ... import ...`
- 包结构与 `__init__.py`。

### 前端类比

| JavaScript / TypeScript | Python                |
| ----------------------- | --------------------- |
| `function fn()`       | `def fn():`         |
| `export` / `import` | `import` / `from` |
| 箭头函数                | `lambda`            |
| npm package             | Python package        |

### 练习

- 封装日期格式化函数。
- 封装接口响应数据校验函数。
- 封装一个 JSON 文件读写模块。
- 把第 2 周项目拆分成多个模块。

### 小项目

实现一个“接口 Mock 生成器”：输入字段配置，生成假数据 JSON。

## 第 4 周：文件、异常与环境管理

目标：能处理真实文件和项目依赖。

### 学习内容

- 文件读写：`open()`。
- JSON 处理：`json`。
- CSV 处理：`csv`。
- 路径处理：`pathlib`。
- 异常处理：`try` / `except` / `finally`。
- 虚拟环境：`venv`。
- 依赖管理：`pip`、`requirements.txt`。

### 前端类比

| 前端概念         | Python 概念                               |
| ---------------- | ----------------------------------------- |
| `package.json` | `requirements.txt` / `pyproject.toml` |
| `node_modules` | 虚拟环境中的 site-packages                |
| `npm install`  | `pip install`                           |
| `fs` 模块      | `pathlib` / `open()`                  |

### 练习

- 读取 JSON 文件并格式化输出。
- 批量重命名文件。
- 将 CSV 转成 JSON。
- 捕获文件不存在、JSON 格式错误等异常。

### 小项目

实现一个“前端路由扫描器”：扫描 `src/views` 目录，输出页面文件清单和路径统计。

## 第 5 周：面向对象与类型提示

目标：理解 Python 的类、对象和类型标注，写出更清晰的代码。

### 学习内容

- 类与实例。
- 构造函数：`__init__`。
- 实例方法、类属性。
- 继承与组合。
- `dataclass`。
- 类型提示：`str`、`int`、`list[str]`、`dict[str, Any]`。
- `mypy` 基础概念。

### 前端类比

| TypeScript        | Python                                       |
| ----------------- | -------------------------------------------- |
| `class User {}` | `class User:`                              |
| `interface`     | `TypedDict` / `Protocol` / `dataclass` |
| 类型注解          | 类型提示                                     |
| `constructor`   | `__init__`                                 |

### 练习

- 用类封装用户信息。
- 用 `dataclass` 定义接口响应模型。
- 写一个 API 响应解析器。
- 给已有函数添加类型提示。

### 小项目

实现一个“需求文档任务拆分器”：输入需求条目，输出任务对象列表，包含标题、优先级、模块、状态。

## 第 6 周：HTTP、接口与 FastAPI

目标：能写后端接口，并和前端联调。

### 学习内容

- 使用 `requests` 调用接口。
- REST API 基础。
- FastAPI 项目结构。
- 路由、请求参数、响应模型。
- Pydantic 数据校验。
- CORS。
- Swagger 文档。

### 前端类比

| 前端概念         | Python / FastAPI |
| ---------------- | ---------------- |
| Axios 请求       | `requests`     |
| Express / NestJS | FastAPI          |
| DTO / Interface  | Pydantic Model   |
| Swagger          | FastAPI 自动文档 |

### 练习

- 写一个 `GET /health` 接口。
- 写一个 `GET /users` 接口。
- 写一个 `POST /users` 接口。
- 用前端页面调用 Python API。

### 小项目

实现一个“前端配置管理 API”：提供配置列表、配置详情、新增配置、删除配置接口。

## 第 7 周：测试、日志与工程化

目标：理解 Python 项目工程化基础。

### 学习内容

- `pytest` 基础。
- 单元测试、参数化测试。
- 日志：`logging`。
- 代码格式化：`black`。
- Import 排序：`isort`。
- 静态检查：`ruff`。
- `.env` 配置读取。

### 前端类比

| 前端工具      | Python 工具   |
| ------------- | ------------- |
| Jest / Vitest | pytest        |
| ESLint        | ruff          |
| Prettier      | black         |
| dotenv        | python-dotenv |

### 练习

- 给数据清洗函数写测试。
- 给 FastAPI 接口写测试。
- 增加日志输出。
- 配置 `black`、`ruff`、`pytest`。

### 小项目

把第 6 周 FastAPI 项目补齐测试、日志和格式化配置。

## 第 8 周：综合项目

目标：完成一个贴近前端工作的 Python 项目。

### 推荐项目 1：前端项目健康检查工具

功能：

- 扫描项目目录。
- 读取 `package.json`。
- 检查依赖版本。
- 统计页面、组件、工具函数数量。
- 输出 Markdown 报告。

### 推荐项目 2：接口文档生成器

功能：

- 读取前端 API 模块。
- 提取接口路径、方法、参数。
- 生成 Markdown 接口文档。

### 推荐项目 3：FastAPI + React / Vue 小后台

功能：

- Python 提供用户、角色、配置接口。
- 前端调用接口展示表格。
- 支持新增、编辑、删除。
- 使用 `pytest` 测试核心接口。

## 每日学习模板

每天按照下面节奏执行：

1. 10 分钟：复习昨天代码。
2. 20 分钟：学习一个新知识点。
3. 30 分钟：完成 2-3 个小练习。
4. 20 分钟：把知识点应用到当前小项目。
5. 10 分钟：写学习笔记，总结 Python 和 JS 的差异。

## 优先掌握清单

如果时间有限，优先学习：

1. 基础语法、数据结构、函数。
2. 文件处理、JSON、CSV。
3. 虚拟环境和依赖管理。
4. `requests` 和 FastAPI。
5. `pytest`。
6. 类型提示和 `dataclass`。

## 暂时可以少学的内容

初期不必深入：

- 元类。
- 装饰器高级用法。
- 多进程、多线程底层细节。
- 复杂算法。
- Django 大型框架。
- 深度学习框架。

## 推荐学习路径

### 阶段 1：脚本能力

学习重点：语法、数据结构、文件、JSON、CSV。

产出：能写自动化脚本。

### 阶段 2：后端接口能力

学习重点：FastAPI、Pydantic、数据库、测试。

产出：能写可联调的 REST API。

### 阶段 3：工程化能力

学习重点：项目结构、日志、配置、测试、部署。

产出：能维护一个小型 Python 服务。

### 阶段 4：专项能力

按兴趣选择：

- 自动化办公。
- 接口测试。
- 数据分析。
- AI 应用开发。
- 爬虫。
- DevOps 脚本。

## 第一天任务

今天只需要完成：

1. 安装 Python 3.11+。
2. 在 VS Code 中确认 Python 插件可用。
3. 创建一个 `python-playground` 文件夹。
4. 创建第一个脚本 `hello.py`。
5. 练习变量、字符串、条件判断和循环。

建议第一天不要学太多，把环境跑通最重要。
