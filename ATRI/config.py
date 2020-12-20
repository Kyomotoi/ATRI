import sys
import time
from pathlib import Path
from datetime import timedelta
from nonebot.log import logger
from ipaddress import IPv4Address
from rich.progress import Progress

from ATRI.utils import loadYaml

CONFIG_PATH = Path('.') / 'ATRI' / 'config' / 'main.config.yml'
config = loadYaml(CONFIG_PATH)


def CheckConfig():
    logger.info('Please stand by, now in checking.')

    len_config = len(config) + len(config['bot']) + len(config['api'])

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

            api = config['api']
            for key in api:
                if not api[key]:
                    print(f"Can't load [{key}] from config.yml")
                    time.sleep(5)
                    sys.exit(0)
                else:
                    progress.update(task_c, advance=1)
                    time.sleep(0.1)


NONEBOT_CONFIG: dict = {
    'host': IPv4Address(config['bot']['host']),
    'port': int(config['bot']['port']),
    'debug': bool(config['bot']['debug']),
    'superusers': config['bot']['superusers'],
    'nickname': set(config['bot']['nickname']),
    'command_start': set(config['bot']['command_start']),
    'command_sep': set(config['bot']['command_sep']),
    'session_expire_timeout':
    timedelta(config['bot']['session_expire_timeout'])
}


PLUGIN_BOT_CONFIG = Path('.') / 'ATRI' / 'config' / 'bot.plugin.yml'
BOT_CONFIG: dict = loadYaml(PLUGIN_BOT_CONFIG)

PLUGIN_GENSHIN_CONFIG = Path('.') / 'ATRI' / 'config' / 'genshin.plugin.yml'
GENSHIN_CONFIG: dict = loadYaml(PLUGIN_GENSHIN_CONFIG)