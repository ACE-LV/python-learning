import os
from dataclasses import dataclass
from pathlib import Path


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        cleaned_value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), cleaned_value)


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    debug: bool
    database_url: str


def get_settings(env_path: Path | None = None) -> Settings:
    if env_path is not None:
        load_env_file(env_path)

    return Settings(
        app_name=os.getenv("APP_NAME", "Day17 Config Demo"),
        app_env=os.getenv("APP_ENV", "dev"),
        debug=parse_bool(os.getenv("DEBUG")),
        database_url=os.getenv("DATABASE_URL", "sqlite:///day17.db"),
    )
