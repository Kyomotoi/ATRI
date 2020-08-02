# -*- coding:utf-8 -*-
import time
COPYRIGHT = (
    r"""====================ATRI | アトリ====================
* CoolQ + NoneBot + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Blog: lolihub.icu
====================================================="""
)
print(COPYRIGHT)
time.sleep(2)

import config # type: ignore
time.sleep(2)
print("ATRI正在苏醒...")

from os import path


if __name__ == '__main__':
    import nonebot
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'ATRI', 'plugins'),
    'ATRI.plugins')
    nonebot.run()