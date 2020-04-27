from nonebot import on_command, CommandSession


@on_command('阿这')
async def _(session: CommandSession):
    await session.send('阿这')

@on_command('喵', aliases=['喵喵', '喵喵喵'])
async def _(session: CommandSession):
    await session.send('喵~')

@on_command('奶宝', aliases=['@๑ ^ ₃•๑', '奶够翘'])
async def _(session: CommandSession):
    await session.send('别叫了别叫了，8在')
