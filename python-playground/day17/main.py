from pathlib import Path

from fastapi import FastAPI

from .settings import get_settings

SETTINGS = get_settings(Path(__file__).with_name(".env"))

app = FastAPI(title=SETTINGS.app_name, debug=SETTINGS.debug)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": SETTINGS.app_env}


@app.get("/config")
def get_config() -> dict[str, object]:
    return {
        "app_name": SETTINGS.app_name,
        "app_env": SETTINGS.app_env,
        "debug": SETTINGS.debug,
        "database_url": SETTINGS.database_url,
    }
