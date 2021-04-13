from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address

from pydantic import BaseConfig

from .utils.yaml import load_yml


CONFIG_PATH = Path('.') / 'config.yml'
config = load_yml(CONFIG_PATH)


class Config(BaseConfig):
    class BotSelfConfig:
        config: dict = config['BotSelfConfig']
        
        host: IPv4Address = IPv4Address(config.get('host', '127.0.0.1'))
        port: int = int(config.get('port', 8080))
        debug: bool = bool(config.get('debug', False))
        superusers: set = set(config.get('superusers', ['1234567890']))
        nickname: set = set(
            config.get('nickname', ['ATRI', 'Atri', 'atri', '亚托莉', 'アトリ']))
        command_start: set = set(config.get('command_start', ['']))
        command_sep: set = set(config.get('command_sep', ['.']))
        session_expire_timeout: timedelta = timedelta(
            config.get('session_expire_timeout', 2))
        session_exciting_time: int = int(config.get('session_exciting_time', 60))
    
    class NetworkPost:
        config: dict = config['NetworkPost']
        
        host: str = config.get('host', '127.0.0.1')
        port: int = int(config.get('port', 8081))
    
    class AdminPage:
        config: dict = config['AdminPage']
        
        host: str = config.get('host', '127.0.0.1')
        port: int = int(config.get('port', 8082))
    
    class NsfwCheck:
        config: dict = config['NsfwCheck']
        
        enabled: bool = bool(config.get('enabled', False))
        passing_rate: float = float(config.get('passing_rate', 0.8))
        host: str = config.get('host', '127.0.0.1')
        port: int = int(config.get('port', 5000))
    
    class SauceNAO:
        config: dict = config['SauceNAO']
        
        key: str = config.get('key', '')


RUNTIME_CONFIG = {
    "host": Config.BotSelfConfig.host,
    "port": Config.BotSelfConfig.port,
    "debug": Config.BotSelfConfig.debug,
    "superusers": Config.BotSelfConfig.superusers,
    "nickname": Config.BotSelfConfig.nickname,
    "command_start": Config.BotSelfConfig.command_start,
    "command_sep": Config.BotSelfConfig.command_sep,
    "session_expire_timeout": Config.BotSelfConfig.session_expire_timeout
}
