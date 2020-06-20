# -*- coding:utf-8 -*-
import nonebot
from AyaBot import config
from AyaBot.plugins import module
from os import path


if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'AyaBot', 'plugins'),
        'AyaBot.plugins')
    nonebot.run()