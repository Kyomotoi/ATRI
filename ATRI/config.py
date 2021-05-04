from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address

from .utils.yaml import load_yml


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


class NetworkPost:
    config: dict = config["NetworkPost"]

    host: str = config.get("host", "127.0.0.1")
    port: int = int(config.get("port", 8081))


class AdminPage:
    config: dict = config["AdminPage"]

    host: str = config.get("host", "127.0.0.1")
    port: int = int(config.get("port", 8082))


class NsfwCheck:
    config: dict = config["NsfwCheck"]

    enabled: bool = bool(config.get("enabled", False))
    passing_rate: int = int(config.get("passing_rate", 85))
    host: str = config.get("host", "127.0.0.1")
    port: int = int(config.get("port", 5000))


class SauceNAO:
    config: dict = config["SauceNAO"]

    key: str = config.get("key", "")


class Setu:
    config: dict = config["Setu"]

    key: str = config.get("key", "")


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
