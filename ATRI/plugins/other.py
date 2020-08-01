# -*- coding:utf-8 -*-
import random
import nonebot
from nonebot import on_command, CommandSession
from nonebot.helpers import render_expression


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS


HELP_REPLY = (
    'ええと...让我想想...',
    '嗯...',
    '阿这',
    '不会使用嘛...ええと'
)


# 论如何将 Python 写出 Java 的味道
# 接下来给各位展示一下
# 咱的屎山

@on_command(
    '抽签',
    only_to_me = False
)
async def _(session: CommandSession):
    await session.send(
        str(
            random.choice(
                [
                    '大凶',
                    '大胸',
                    '小凶',
                    '小胸',
                    '凶',
                    '吉',
                    '中吉',
                    '大吉',
                    '特大吉',
                    '超特大吉'
                ]
            )
        )
    )

@on_command(
    '掷骰子',
    aliases = [
        '扔骰子',
        '骰子'
    ],
    only_to_me = False
)
async def _(session: CommandSession):
    await session.send(
        str(
            random.randint(
                1,6
            )
        )
    )

@on_command(
    '关于',
    aliases = [
        '关于机器人'
    ],
    only_to_me = False
)
async def _(session: CommandSession):
    await session.send(
        f"""想了解ATRI嘛
        写出咱的是Kyomotoi
        他的主页:https://lolihub.icu
        项目地址:https://github.com/Kyomotoi/ATRI
        欢迎star~w!"""
    )

@on_command(
    'help',
    aliases = [
        '帮助',
        '如何使用ATRI',
        '机器人帮助'
    ],
    only_to_me = False
)
async def _(session: CommandSession):
    await session.send(
        f"""{render_expression(HELP_REPLY)}
        看这吧！
        https://lolihub.icu/#/robot/user"""
    )