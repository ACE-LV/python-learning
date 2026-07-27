from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Day13 Depends Auth")

API_TOKEN = "dev-token"


class UserPublic(BaseModel):
    id: int
    name: str
    role: str


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)


USERS = [
    {"id": 1, "name": "Alice", "role": "frontend"},
    {"id": 2, "name": "Bob", "role": "backend"},
]
NOTES: list[dict[str, object]] = []
NEXT_NOTE_ID = 1


def require_token(authorization: str | None = Header(default=None)) -> None:
    expected = f"Bearer {API_TOKEN}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )


@app.get("/public/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/me", response_model=UserPublic)
def get_me(_: None = Depends(require_token)) -> dict[str, object]:
    return USERS[0]


@app.get("/admin/users", response_model=list[UserPublic])
def list_users(_: None = Depends(require_token)) -> list[dict[str, object]]:
    return USERS


@app.post("/notes")
def create_note(payload: NoteCreate, _: None = Depends(require_token)) -> dict[str, object]:
    global NEXT_NOTE_ID

    note = {"id": NEXT_NOTE_ID, "title": payload.title, "content": payload.content}
    NOTES.append(note)
    NEXT_NOTE_ID += 1
    return note


@app.get("/notes")
def list_notes(_: None = Depends(require_token)) -> list[dict[str, object]]:
    return NOTES
