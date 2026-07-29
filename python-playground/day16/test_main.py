import pytest
from fastapi.testclient import TestClient
from main import app, reset_users


@pytest.fixture()
def client() -> TestClient:
    # fixture 是 pytest 提供的“测试前准备函数”。
    # 每个测试函数参数里写 client，pytest 就会先执行这里，再把返回值传进去。
    # 这里先 reset_users()，保证每个测试都从同一份初始数据开始。
    reset_users()
    # TestClient 可以不用真的启动 uvicorn，就能像浏览器/前端一样请求 FastAPI app。
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    # 测试公开健康检查接口。
    response = client.get("/health")

    # 断言状态码。
    assert response.status_code == 200
    # 断言响应 JSON 内容。
    assert response.json() == {"status": "ok"}


def test_list_users(client: TestClient) -> None:
    # 测试初始用户列表。
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Alice", "role": "frontend"}]


def test_create_user(client: TestClient) -> None:
    # 测试创建用户成功场景。
    response = client.post("/users", json={"name": "Bob", "role": "backend"})

    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "Bob", "role": "backend"}


def test_get_missing_user_returns_404(client: TestClient) -> None:
    # 测试业务资源不存在时返回 404。
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_with_invalid_payload_returns_422(client: TestClient) -> None:
    # 测试请求体格式/字段校验失败时返回 422。
    # 这里 name 为空字符串，违反 Field(min_length=1)。
    response = client.post("/users", json={"name": "", "role": "backend"})

    assert response.status_code == 422
