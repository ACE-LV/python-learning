import os
from typing import Literal

from anthropic import Anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from openai import OpenAI
from pydantic import BaseModel, Field

Provider = Literal["openai", "anthropic", "gemini"]

DEFAULT_MODELS: dict[Provider, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "gemini": "gemini-1.5-flash",
}

app = FastAPI(title="Day19 Multi Provider AI Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    system_prompt: str | None = Field(default=None, max_length=2000)
    model: str | None = Field(default=None, min_length=1, max_length=120)
    temperature: float = Field(default=0.2, ge=0, le=2)


class ChatResponse(BaseModel):
    provider: Provider
    model: str
    reply: str


def _required_api_key(provider: Provider) -> str:
    key_name = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
    }[provider]
    api_key = os.getenv(key_name)
    if not api_key:
        raise HTTPException(status_code=400, detail=f"{key_name} is required")
    return api_key


def _ask_openai(payload: ChatRequest) -> str:
    client = OpenAI(api_key=_required_api_key("openai"))
    model_name = payload.model or DEFAULT_MODELS["openai"]
    messages = []
    if payload.system_prompt:
        messages.append({"role": "system", "content": payload.system_prompt})
    messages.append({"role": "user", "content": payload.message})
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=payload.temperature,
    )
    content = response.choices[0].message.content
    if not content:
        raise HTTPException(status_code=502, detail="OpenAI returned empty content")
    return content


def _ask_anthropic(payload: ChatRequest) -> str:
    client = Anthropic(api_key=_required_api_key("anthropic"))
    model_name = payload.model or DEFAULT_MODELS["anthropic"]
    response = client.messages.create(
        model=model_name,
        max_tokens=1024,
        temperature=payload.temperature,
        system=payload.system_prompt or "",
        messages=[{"role": "user", "content": payload.message}],
    )
    text_parts = [block.text for block in response.content if block.type == "text"]
    if not text_parts:
        raise HTTPException(status_code=502, detail="Anthropic returned empty content")
    return "\n".join(text_parts)


def _ask_gemini(payload: ChatRequest) -> str:
    client = genai.Client(api_key=_required_api_key("gemini"))
    model_name = payload.model or DEFAULT_MODELS["gemini"]
    prompt = payload.message
    if payload.system_prompt:
        prompt = f"{payload.system_prompt}\n\nUser: {payload.message}"
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={"temperature": payload.temperature},
    )
    text = response.text
    if not text:
        raise HTTPException(status_code=502, detail="Gemini returned empty content")
    return text


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/providers")
def providers() -> dict[str, dict[str, str]]:
    return {
        provider: {
            "default_model": model_name,
            "api_key_env": {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "gemini": "GEMINI_API_KEY",
            }[provider],
        }
        for provider, model_name in DEFAULT_MODELS.items()
    }


@app.post("/chat/{provider}", response_model=ChatResponse)
def chat(provider: Provider, payload: ChatRequest) -> ChatResponse:
    model_name = payload.model or DEFAULT_MODELS[provider]
    if provider == "openai":
        reply = _ask_openai(payload)
    elif provider == "anthropic":
        reply = _ask_anthropic(payload)
    else:
        reply = _ask_gemini(payload)
    return ChatResponse(provider=provider, model=model_name, reply=reply)
