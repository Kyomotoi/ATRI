# -*- coding:utf-8 -*-
import time
COPYRIGHT = (
    r"""ATRI | アトリ
Copyright © 2018-2020 Kyomotoi,All Rights Reserved
Project: https://github.com/Kyomotoi/Aya
Blog: lolihub.icu
==================================================="""
)
print(COPYRIGHT)
time.sleep(0)


from ATRIbot import config
time.sleep(0)
print("开始执行主程序...RCnb!")


time.sleep(0)
from os import path
from ATRIbot.plugins import module


if __name__ == '__main__':
    import nonebot
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'ATRIbot', 'plugins'),
        'ATRIbot.plugins')
    nonebot.run()