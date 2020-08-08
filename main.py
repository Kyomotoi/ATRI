import time
COPYRIGHT = (
    r"""====================ATRI | アトリ====================
* OPQBot + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Blog: blog.lolihub.icu
====================================================="""
)
print(COPYRIGHT)
time.sleep(2)


import config_ # type: ignore
from iotbot import *
bot = IOTBOT(
    qq = config_.BOT_QQ(),
    host = str(config_.HOST()),
    port = str(config_.PORT()),
    log = True, # 可关，看个人需求，如是开发者此项建议开启
    use_plugins = True # 请勿动！
)
action = Action(bot)
master = config_.MASTER()
time.sleep(2)
print("ATRI正在苏醒...")


@bot.on_group_msg
def on_group_msg(ctx: GroupMsg):
    # 不处理自身消息
    if ctx.FromUserId == ctx.CurrentQQ:
        return
    content = ctx.Content  # type: str

    # 刷新插件
    if ctx.FromUserId == master and content == '重启螃蟹服务器':
        time.sleep(1)
        if bot.refresh_plugins():
            action.send_group_text_msg(ctx.FromGroupId, '完成！') # type: ignore
        else:
            action.send_group_text_msg(ctx.FromGroupId, '失败了...') # type: ignore
        time.sleep(1)
        return


if __name__ == "__main__":
    bot.run()