import random
import nonebot
import warnings
from nonebot import on_command, CommandSession
from nonebot.helpers import render_expression

import config
from ATRI.modules.time import sleepTime
from ATRI.modules.funcControl import checkNoob


bot = nonebot.get_bot()
master = config.SUPERUSERS

def countX(lst, x):
    warnings.simplefilter('ignore', ResourceWarning)
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


HELP_REPLY = (
    'ええと...让我想想...',
    '嗯...',
    '阿这',
    '不会使用嘛...ええと'
)


@on_command('抽签', only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if sleepTime():
            await session.send(sleepTime())
        else:
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

@on_command('掷骰子', aliases = ['扔骰子', '骰子'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if sleepTime():
            await session.send(sleepTime())
        else:
            await session.send(
                str(
                    random.randint(
                        1,6
                    )
                )
            )

@on_command('关于', aliases = ['关于'])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        await session.send(
            """想了解ATRI嘛
写出咱的是Kyomotoi
他的主页:https://blog.lolihub.icu/
项目地址:https://github.com/Kyomotoi/ATRI
欢迎star~w!"""
        )

@on_command('help', aliases = ['帮助', '如何使用ATRI', '机器人帮助', '菜单'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        await session.send(
            f"""{render_expression(HELP_REPLY)}
请仔细阅读文档哦~~https://blog.lolihub.icu/#/ATRI/user"""
        )


RepoList = []
@on_command('report', aliases = ['来杯红茶'], only_to_me = True)
async def EMMAAAA(session: CommandSession):
    global RepoList
    h_type = session.event.detail_type
    msg = session.current_arg.strip()
    user = session.event.user_id
    group = session.event.group_id

    if not msg:
        msg = session.get('message', prompt='请键入需要反馈的信息')

    RepoList.append(user)

    if countX(RepoList, user) == 5:
        session.finish('您今天已经喝了5杯红茶啦！明天再来吧！')

    if h_type == 'group':
        await bot.send_private_msg(
            user_id = master,
            message = f"来自群[{group}]，用户[{user}]的反馈：\n{msg}"
        ) # type: ignore
    
    elif h_type == 'private':
        await bot.send_private_msg(
            user_id = master,
            message = f"来自用户[{user}]的反馈：\n{msg}"
        ) # type: ignore

@EMMAAAA.args_parser
async def _(session: CommandSession):
    if not session.is_first_run and session.current_arg.startswith('算了'):
        session.switch(session.current_arg[len('算了'):])

@nonebot.scheduler.scheduled_job(
    'cron',
    hour = 0,
    misfire_grace_time = 10 
)
async def _():
    global RepoList
    try:
        RepoList = []
    except:
        await bot.send_private_msg(user_id = master, message = f'红茶重置失败...请手动重启ATRI以重置红茶...') # type: ignore
        return
    await bot.send_private_msg(user_id = master, message = '红茶重置成功！') # type: ignore