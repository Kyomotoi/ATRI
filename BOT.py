import time
COPYRIGHT = (
    r"""====================[ATRI | アトリ]====================
* Mirai + NoneBot + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Blog: blog.lolihub.icu
======================================================="""
)
print(COPYRIGHT)
time.sleep(2)

import config
print("ATRI正在苏醒...")
time.sleep(2)

from os import path


if __name__ == '__main__':
    import nonebot
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'ATRI', 'plugins'),
    'ATRI.plugins')
    nonebot.run()