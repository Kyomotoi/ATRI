# -*- coding:utf-8 -*-
import time
COPYRIGHT = (
    r"""AyaCoolQBot
Copyright © 2018-2020 Kyomotoi,All Rights Reserved
Project: https://github.com/Kyomotoi/Aya
Blog: lolihub.icu
==================================================="""
)
print(COPYRIGHT)
time.sleep(2)


from AyaBot import config
time.sleep(2)
print("开始执行主程序...RCnb!")


time.sleep(2)
from os import path
from AyaBot.plugins import module


if __name__ == '__main__':
    import nonebot
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'AyaBot', 'plugins'),
        'AyaBot.plugins')
    nonebot.run()