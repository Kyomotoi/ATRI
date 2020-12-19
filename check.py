#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   check.py
@Time    :   2020/11/07 14:30:34
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import os
import sys
import time
import pkg_resources
from pathlib import Path
from rich.progress import Progress
from ATRI.utils.utils_yml import load_yaml

CONFIG_PATH = Path('.') / 'config.yml'
config = load_yaml(CONFIG_PATH)


class CheckATRI():
    """运行前检查必要条件"""
    def checkConfig(self) -> None:
        """检查配置文件是否填写完整"""
        len_config = len(config) + len(config['bot']) + len(
            config['api']) + len(config['html'])

        with Progress() as progress:
            task = progress.add_task("[cyan]Checking Config...",
                                     total=len_config)

            while not progress.finished:
                # 检查基本配置
                bot = config['bot']
                for key in bot:
                    if key == 'debug':
                        if bot['debug'] != 0:
                            print('DEBUG now is open.')
                            progress.update(task, advance=1)
                            time.sleep(0.1)
                    else:
                        if not bot[key]:
                            print(f"Can't load [{key}] from config.yml")
                            time.sleep(5)
                            sys.exit(0)

                        else:
                            progress.update(task, advance=1)
                            time.sleep(0.1)

                # 检查接口配置
                api = config['api']
                for key in api:
                    if not api[key]:
                        print(f"Can't load [{key}] from config.yml")
                        time.sleep(5)
                        sys.exit(0)
                    else:
                        progress.update(task, advance=1)
                        time.sleep(0.1)

                # 检查网页配置
                html = config['html']
                for key in html:
                    if not html[key]:
                        print(f"Can't load [{key}] from config.yml")
                        time.sleep(5)
                        sys.exit(0)
                    else:
                        progress.update(task, advance=1)
                        time.sleep(0.1)
