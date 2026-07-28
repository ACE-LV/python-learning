# Python 第十九天：多模型 AI 接口接入（OpenAI / Anthropic / Gemini）

## 今日目标

用一个 FastAPI 服务统一接入三个 AI 提供商，前端只需要调用同一种接口格式。

你需要掌握：

1. 通过环境变量管理 API Key。
2. 用同一套请求体切换不同 provider。
3. 让前端只改 URL 就能切模型。

## 安装依赖

```powershell
python -m pip install fastapi uvicorn openai anthropic google-genai
```

## 配置环境变量（PowerShell 当前终端）

```powershell
$env:OPENAI_API_KEY="你的-openai-key"
$env:ANTHROPIC_API_KEY="你的-anthropic-key"
$env:GEMINI_API_KEY="你的-gemini-key"
```

## 启动服务

```powershell
python -m uvicorn day19.main:app --reload --app-dir .\python-playground
```

## 常用接口

- `GET /health`：服务健康检查
- `GET /providers`：查看 provider 默认模型和 API Key 环境变量名
- `POST /chat/{provider}`：统一聊天接口，`provider` 支持 `openai` / `anthropic` / `gemini`

### 请求示例

```json
{
  "message": "请用 3 句话解释 Python 装饰器",
  "system_prompt": "你是一个给前端讲 Python 的老师",
  "temperature": 0.2
}
```
