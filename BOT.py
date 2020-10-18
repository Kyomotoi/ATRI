#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   bot.py
@Time    :   2020/10/11 14:36:01
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import time
COPYRIGHT = (
    r"""====================[ATRI | アトリ]====================
* Mirai + NoneBot2 + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Blog: blog.lolihub.icu
=======================================================""")
print(COPYRIGHT)
time.sleep(2)

import nonebot

nonebot.init()
app = nonebot.get_asgi()

nonebot.load_plugins("ATRI/plugins")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
