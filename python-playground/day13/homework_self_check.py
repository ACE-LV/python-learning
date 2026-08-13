"""Day13 homework 的最小自测脚本。

不使用 FastAPI TestClient，避免额外依赖 httpx。
"""

from fastapi import HTTPException

import homework


def assert_http_error(func, expected_status_code: int, *args, **kwargs) -> None:
    try:
        func(*args, **kwargs)
    except HTTPException as exc:
        assert exc.status_code == expected_status_code
    else:
        raise AssertionError(f"Expected HTTP {expected_status_code}")


def main() -> None:
    homework.init_db()

    assert homework.health() == {"status": "ok"}

    assert_http_error(homework.require_token, 401, None)
    assert_http_error(homework.require_token, 401, "Bearer wrong-token")
    assert homework.require_token("Bearer dev-token") is None

    assert_http_error(homework.require_admin_token, 401, None)
    assert_http_error(homework.require_admin_token, 403, "Bearer dev-token")
    assert homework.require_admin_token("Bearer admin-token") is None

    assert len(homework.get_notes()) >= 1
    assert len(homework.get_admin_users()) >= 1

    print("Day13 homework self-check passed.")


if __name__ == "__main__":
    main()
