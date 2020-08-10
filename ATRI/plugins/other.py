# -*- coding:utf-8 -*-
import time
import random
import nonebot
from nonebot import on_command, CommandSession
from nonebot.helpers import render_expression

import config # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()


HELP_REPLY = (
    'ええと...让我想想...',
    '嗯...',
    '阿这',
    '不会使用嘛...ええと'
)


MENU_REPO = '''
======================
ATRI 使用说明
======================
* 发送[]内的关键词以激活相关指令
* 命令前带'@'表示需要atBOT
* 命令前带'FIX'表示暂时失效
* 管理类使用方法会附在网页版的使用手册

======[基本功能]======
[以图搜番] 字面意思
[FIX 本子] 搜索本子
[一言] 字面意思
[P站搜图] 以Pid码搜索P站的图片
[画师] 以画师ID搜索P站画师的作品
[P站排行榜] 获取实时更新的P站排行榜
[来份涩图] 获取一张涩图
========[HELP]========
[帮助] 获取网页版使用手册
[菜单] 打开本页面
[关于] 获取项目、作者信息
[@ 来杯红茶] 向作者反馈
=======[小功能]=======
[掷骰子] 1~6的随机数
[抽签] 抽取今日运势
'''.strip()

MENU_AND = '''
* 由于本项目以及本人一些个人原因，出现Bug请及时反馈
* 本项目开源，可自行搭建，方法附在网页版使用手册中
* 如有意愿fork本项目，提交修改，作者会非常感动
* 运行示例、开发、维护需要成本，作者希望能被赞助
* Star、提交Issus以及Fork并提交修改意见是本项目继续下去的动力
* 运行时请适当使用，滥用可能会导致账号被封禁
'''.strip()


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
他的主页:https://blog.lolihub.icu
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
发送：菜单
或看这吧！
https://lolihub.icu/#/robot/user"""
        )

@on_command(
    'menu',
    aliases = [
        '菜单'
    ],
    only_to_me = False
)
async def _(session: CommandSession):
    await session.send(MENU_REPO)
    time.sleep(0.5)
    await session.send(MENU_AND)

@on_command(
    'report',
    aliases = [
        '来杯红茶'
    ],
    only_to_me = True
)
async def _(session: CommandSession):
    msg = session.current_arg.strip()
    user = session.event.user_id
    group = session.event.group_id
    if not msg:
        msg = session.get('message', prompt='请键入需要反馈的信息')
    
    await bot.send_private_msg(
        user_id = master,
        message = f"来自群[{group}]，用户[{user}]的反馈：\n{msg}"
    ) # type: ignore