from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

# 第 13 天主题：FastAPI 依赖注入 Depends + 最小 token 鉴权。
app = FastAPI(title="Day13 Depends Auth")

# 演示用 token。
# 真实项目不会把 token 写死在代码里，通常会从环境变量、配置中心或登录系统生成。
API_TOKEN = "dev-token"


class UserPublic(BaseModel):
    # 返回给前端的用户信息结构。
    # response_model=UserPublic 会保证接口只返回这些公开字段。
    id: int
    name: str
    role: str


class NoteCreate(BaseModel):
    # 创建 note 的请求体。
    # title/content 都有长度限制，非法请求会在进入接口函数前返回 422。
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)


# 用内存数据模拟“当前用户列表”。
USERS = [
    {"id": 1, "name": "Alice", "role": "frontend"},
    {"id": 2, "name": "Bob", "role": "backend"},
]

# 用内存列表模拟需要登录后才能访问的 note 数据。
NOTES: list[dict[str, object]] = []

# 模拟 note 自增 ID。
NEXT_NOTE_ID = 1


def require_token(authorization: str | None = Header(default=None)) -> None:
    # 这是一个依赖函数 dependency。
    # 谁在接口参数里写 Depends(require_token)，FastAPI 就会在执行接口函数前先运行它。

    # Header(default=None) 表示从 HTTP 请求头里读取 Authorization。
    # 如果前端没传 Authorization，这里就是 None。
    # 请求头示例：Authorization: Bearer dev-token
    expected = f"Bearer {API_TOKEN}"
    if authorization != expected:
        # 401 表示“没有登录/认证失败”。
        # 注意：这和 403 不一样；403 是“已登录但没有权限”。
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )


@app.get("/public/health")
def health_check() -> dict[str, str]:
    # 公开接口：没有 Depends(require_token)，所以不需要 token。
    return {"status": "ok"}


@app.get("/me", response_model=UserPublic)
def get_me(_: None = Depends(require_token)) -> dict[str, object]:
    # 受保护接口：调用前会先执行 require_token。
    # 参数名写成 _ 表示我们不关心依赖函数的返回值，只关心它能否通过校验。
    # token 不对时，require_token 会直接抛 401，get_me 的函数体不会执行。
    return USERS[0]


@app.get("/admin/users", response_model=list[UserPublic])
def list_users(_: None = Depends(require_token)) -> list[dict[str, object]]:
    # 管理员用户列表接口，目前用同一个 require_token 做最小鉴权。
    # practice 里会进一步练习 require_admin_token，把普通 token 和 admin token 区分开。
    return USERS


@app.post("/notes")
def create_note(payload: NoteCreate, _: None = Depends(require_token)) -> dict[str, object]:
    # 创建 note 也需要 token。
    # FastAPI 执行顺序：先校验 token 依赖，再校验/解析 payload，然后进入函数体。
    global NEXT_NOTE_ID

    note = {"id": NEXT_NOTE_ID, "title": payload.title, "content": payload.content}
    NOTES.append(note)
    NEXT_NOTE_ID += 1
    return note


@app.get("/notes")
def list_notes(_: None = Depends(require_token)) -> list[dict[str, object]]:
    # 查询 notes 也需要 token。
    return NOTES
