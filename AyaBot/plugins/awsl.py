import random
from nonebot import on_command, CommandSession


@on_command('阿这', only_to_me=False)
async def _(session: CommandSession):
    await session.send('阿这')

@on_command('喵', aliases=['喵喵', '喵喵喵'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('喵~')

@on_command('奶宝', aliases=['@๑ ^ ₃•๑', '奶够翘'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('别叫了别叫了，8在')

@on_command('抽签', only_to_me=False)
async def _(session: CommandSession):
    await session.send(str(random.choice(['大凶', '小凶', '凶', '吉', '小吉', '中吉', '大吉'])))