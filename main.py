# -*- coding:utf-8 -*-
# from iotbot import IOTBOT, Action, GroupMsg
from iotbot import *


bot_qq = 2791352599

bot = IOTBOT(
    qq = bot_qq,
    host = 'http://8.210.1.20',
    port = 8888,
    log = True,
    use_plugins = True
)
action = Action(bot)


@bot.on_group_msg
def on_group_msg(ctx: GroupMsg):
    # 不处理自身消息
    if ctx.FromUserId == ctx.CurrentQQ:
        return


if __name__ == "__main__":
    bot.run()