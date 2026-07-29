import os
from dataclasses import dataclass
from pathlib import Path

# 第 17 天主题：配置与环境变量。
# 目标：不要把环境相关配置写死在业务代码里，而是从环境变量或 .env 文件读取。


def parse_bool(value: str | None, default: bool = False) -> bool:
    # 环境变量读出来永远是字符串或 None。
    # 这个函数把常见的 true 写法转换成 Python bool。
    # 例如 DEBUG=true / DEBUG=1 / DEBUG=yes 都会变成 True。
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_env_file(path: Path) -> None:
    # 读取 .env 文件，把里面的 KEY=VALUE 写入 os.environ。
    # .env.example 是模板，不放真实密码；.env 才是本机真实配置，通常不提交 git。
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        # 跳过空行、注释行、不是 KEY=VALUE 格式的行。
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        # 去掉空格和外层引号，支持 APP_NAME="Demo" 这种写法。
        cleaned_value = value.strip().strip('"').strip("'")
        # setdefault 表示：如果系统环境变量已经有这个 key，就不要用 .env 覆盖。
        # 这样部署环境里的真实环境变量优先级更高。
        os.environ.setdefault(key.strip(), cleaned_value)


@dataclass(frozen=True)
class Settings:
    # Settings 是集中配置对象。
    # frozen=True 表示创建后不建议修改，避免运行中配置被随手改乱。
    app_name: str
    app_env: str
    debug: bool
    database_url: str


def get_settings(env_path: Path | None = None) -> Settings:
    # 统一读取配置的入口。
    # main.py 只调用 get_settings，不直接到处 os.getenv，这样配置来源集中管理。
    if env_path is not None:
        load_env_file(env_path)

    return Settings(
        # os.getenv(key, default) 表示：有环境变量就用环境变量，没有就用默认值。
        app_name=os.getenv("APP_NAME", "Day17 Config Demo"),
        app_env=os.getenv("APP_ENV", "dev"),
        # DEBUG 需要从字符串转换成 bool，不能直接 bool(os.getenv("DEBUG"))。
        # 因为 bool("false") 也是 True。
        debug=parse_bool(os.getenv("DEBUG")),
        database_url=os.getenv("DATABASE_URL", "sqlite:///day17.db"),
    )
