import sys
import time
from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address
from rich.progress import Progress

from .log import logger
from .utils import load_yaml

CONFIG_PATH = Path('.') / 'ATRI' / 'config' / 'main.config.yml'
config = load_yaml(CONFIG_PATH)


def check_config() -> None:
    logger.info('Please stand by, now in checking type.')

    len_config = len(config) + len(config['bot'])

    with Progress() as progress:
        task_c = progress.add_task("[cyan]Checking config...",
                                   total=len_config)

        while not progress.finished:
            bot = config['bot']
            for key in bot:
                if key == 'debug':
                    if bot['debug'] != 0:
                        print('DEBUG now is open.')
                        progress.update(task_c, advance=1)
                        time.sleep(0.1)
                else:
                    if not bot[key]:
                        print(f"Can't load [{key}] from config.yml")
                        time.sleep(5)
                        sys.exit(0)
                    else:
                        progress.update(task_c, advance=1)
                        time.sleep(0.1)
    

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

VERSION = config['version']

RUNTIME_CONFIG: dict = {
        'host': IPv4Address(config['bot'].get('host', '127.0.0.1')),
        'port': int(config['bot'].get('port', 8080)),
        'debug': bool(config['bot'].get('debug', False)),
        'superusers': config['bot'].get('superusers', [1234567890]),
        'nickname': set(
            config['bot'].get(
                'nickname', ['ATRI', 'Atri', 'atri', '亚托莉', 'アトリ'])),
        'command_start': set(config['bot'].get('command_start', ['', '/'])),
        'command_sep': set(config['bot'].get('command_sep', ['.'])),
        'session_expire_timeout': timedelta(
            config['bot'].get('session_expire_timeout', 2))
    }

PLUGIN_BOT_CONFIG = Path('.') / 'ATRI' / 'config' / 'character.plugin.yml'
BOT_CONFIG: dict = load_yaml(PLUGIN_BOT_CONFIG)

PLUGIN_HITOKOTO_CONFIG = Path('.') / 'ATRI' / 'config' / 'hitokoto.plugin.yml'
HITOKOTO_CONFIG: dict = load_yaml(PLUGIN_HITOKOTO_CONFIG)

PLUGIN_UTILS_CONFIG = Path('.') / 'ATRI' / 'config' / 'utils.plugin.yml'
UTILS_CONFIG: dict = load_yaml(PLUGIN_UTILS_CONFIG)

PLUGIN_CURSE_CONFIG = Path('.') / 'ATRI' / 'config' / 'curse.plugin.yml'
CURSE_CONFIG: dict = load_yaml(PLUGIN_CURSE_CONFIG)

PLUGIN_SETU_CONFIG = Path('.') / 'ATRI' / 'config' / 'setu.plguin.yml'
SETU_CONFIG: dict = load_yaml(PLUGIN_SETU_CONFIG)
