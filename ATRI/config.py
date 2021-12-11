import yaml
from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address


def load_yml(file: Path, encoding="utf-8") -> dict:
    with open(file, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data


CONFIG_PATH = Path(".") / "config.yml"
config = load_yml(CONFIG_PATH)


class BotSelfConfig:
    config: dict = config["BotSelfConfig"]

    host: IPv4Address = IPv4Address(config.get("host", "127.0.0.1"))
    port: int = int(config.get("port", 8080))
    debug: bool = bool(config.get("debug", False))
    superusers: set = set(config.get("superusers", ["1234567890"]))
    nickname: set = set(config.get("nickname", ["ATRI", "Atri", "atri", "亚托莉", "アトリ"]))
    command_start: set = set(config.get("command_start", [""]))
    command_sep: set = set(config.get("command_sep", ["."]))
    session_expire_timeout: timedelta = timedelta(
        seconds=config.get("session_expire_timeout", 60)
    )
    proxy: str = config.get("proxy", None)


class SauceNAO:
    config: dict = config["SauceNAO"]

    key: str = config.get("key", "")


class ChatterBot:
    config: dict = config["ChatterBot"]

    mongo_database_uri: str = config.get("mongo_database_uri", None)
    maximum_similarity_threshold: float = float(config.get("maximum_similarity_threshold", 0.05))
    default_response: set = set(config.get("default_response", ["咱听不明白(o_ _)ﾉ"]))
    group_random_response_rate: float = float(config.get("group_random_response_rate", 0.1))

RUNTIME_CONFIG = {
    "host": BotSelfConfig.host,
    "port": BotSelfConfig.port,
    "debug": BotSelfConfig.debug,
    "superusers": BotSelfConfig.superusers,
    "nickname": BotSelfConfig.nickname,
    "command_start": BotSelfConfig.command_start,
    "command_sep": BotSelfConfig.command_sep,
    "session_expire_timeout": BotSelfConfig.session_expire_timeout,
}
