import time
from iotbot import *


bot_qq = 
bot = IOTBOT(
    qq = bot_qq,
    host = '',
    port = ,
    log = True,
    use_plugins = True
)
action = Action(bot)

master = 


@bot.on_group_msg
def on_group_msg(ctx: GroupMsg):
    # 不处理自身消息
    if ctx.FromUserId == ctx.CurrentQQ:
        return
    content = ctx.Content  # type: str

    # 刷新插件
    if ctx.FromUserId == master and content == '刷新插件':
        time.sleep(1)
        if bot.refresh_plugins():
            action.send_group_text_msg(ctx.FromGroupId, '完成！') # type: ignore
        else:
            action.send_group_text_msg(ctx.FromGroupId, '失败了...') # type: ignore
        time.sleep(1)
        return


if __name__ == "__main__":
    bot.run()