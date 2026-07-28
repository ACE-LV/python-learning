# Python 第十七天：配置与环境变量

## 今日目标

把写死在代码里的配置抽出来，用环境变量控制不同环境。

你需要掌握：

1. 用 `os.getenv` 读取环境变量。
2. 用 `.env.example` 记录配置模板。
3. 把字符串转换成 bool/int。
4. 避免把真实密钥写进代码。

## 学习顺序

1. 阅读 `.env.example`。
2. 阅读 `settings.py`。
3. 运行 `main.py`。
4. 修改环境变量后重新运行。
5. 完成 `practice.py`。
6. 完成 `homework.py`。
7. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day17.main:app --reload
```

## PowerShell 临时设置环境变量

```powershell
$env:APP_ENV = "uat"
$env:DEBUG = "true"
```

## 今日验收标准

- 能解释为什么配置不应该散落在业务代码里。
- 能区分 `.env.example` 和真实 `.env`。
- 能读取当前环境配置并通过接口返回。
