from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address

from .utils.yaml import load_yml


CONFIG_PATH = Path('.') / 'config.yml'
config = load_yml(CONFIG_PATH)
nonebot_config = config['BotSelfConfig']


COPYRIGHT = """
 █████     ████████     ██████       ██
██   ██       ██        ██   ██      ██
███████       ██        ██████       ██
██   ██       ██        ██   ██      ██
██   ██       ██        ██   ██      ██
=========================================
Copyright © 2021 Kyomotoi, All Rights Reserved.
Project: https://github.com/Kyomotoi/ATRI
"""

VERSION = "YHN-001-A01"

RUNTIME_CONFIG = {
    "host": IPv4Address(nonebot_config.get('host', '127.0.0.1')),
    "port": int(nonebot_config.get('port', '8080')),
    "debug": bool(nonebot_config.get('debug', False)),
    "superusers": set(nonebot_config.get('superusers', ["1234567890"])),
    "nickname": set(
        nonebot_config.get(
            'nickname',
            ['ATRI', 'Atri', 'atri', '亚托莉', 'アトリ']
        )
    ),
    "command_start": set(nonebot_config.get('command_start', ['', '/'])),
    "command_sep": set(nonebot_config.get('command_sep', ['.'])),
    "session_expire_timeout": timedelta(
        nonebot_config.get('session_expire_timeout', 2)
    )
}
