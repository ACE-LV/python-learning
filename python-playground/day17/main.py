from pathlib import Path

from fastapi import FastAPI

from .settings import get_settings

# 从和当前文件同目录的 .env 读取配置。
# with_name(".env") 的意思是：把 main.py 这个文件名替换成 .env。
SETTINGS = get_settings(Path(__file__).with_name(".env"))

# app 的 title/debug 都来自集中配置。
# 这样不同环境只改 .env 或环境变量，不需要改 Python 代码。
app = FastAPI(title=SETTINGS.app_name, debug=SETTINGS.debug)


@app.get("/health")
def health_check() -> dict[str, str]:
    # health 接口返回当前环境，方便你确认服务到底跑在 dev/uat/prod 哪个配置下。
    return {"status": "ok", "environment": SETTINGS.app_env}


@app.get("/config")
def get_config() -> dict[str, object]:
    # 演示配置读取结果。
    # 注意：真实项目不要把 SECRET_KEY、密码、token 这类敏感值原样返回给前端。
    return {
        "app_name": SETTINGS.app_name,
        "app_env": SETTINGS.app_env,
        "debug": SETTINGS.debug,
        "database_url": SETTINGS.database_url,
    }
