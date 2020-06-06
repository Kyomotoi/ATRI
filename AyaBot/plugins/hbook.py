import re
import nonebot
from aiohttp import ClientSession
from nonebot import on_command, CommandSession


async def post_bytes(url, headers=None,data=None):
    async with ClientSession() as asyncsession:
        async with asyncsession.post(url,headers=headers,data=data) as response:
            b = await response.read()
    return b


hbook_switch = True
@on_command('switch', aliases=['开启', '关闭'], only_to_me=False)
async def _(session: CommandSession):
    if session.ctx['user_id'] in session.bot.config.SUPERUSERS:
        command = session.ctx['raw_message'].split(' ', 1)
        swtich = command[0]
        plugins = command[1]
        global hbook_switch
        if swtich == '开启':
            if plugins == '本子':
                hbook_switch = True
            else:
                await session.send('检查一下是否输错了呢')
        else:
            if plugins == '本子':
                hbook_switch = False
            else:
                await session.send('检查一下是否输错了呢')
        await session.send('完成')
    else:
        await session.send('恁哪位?')


@on_command('hbook', aliases=['本子', '找本子', '本子查询'], only_to_me=False)
async def _(session: CommandSession):
    if hbook_switch:
        h_msg = session.current_arg.strip()
        if not h_msg:
            h_msg = session.get('message', prompt='要冲了吗？速发关键词')
        h_type = session.ctx['message_type']
        h_qq = session.ctx['user_id']
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        keyword = {'show':'title,titleen,tags','keyboard':h_msg}
        responce = await post_bytes('https://b-upp.com/search/', headers=header, data=keyword)
        responce = responce.decode()
        if '没有搜索到相关的内容' in responce:
            n_msg = '...似乎没有找到[{}]相关的本子呢'.format(h_msg)
            await session.send(message=n_msg)
        else:
            p = '<a href="(.*?)" target="_blank" title="(.*?)">'
            data = re.findall(p,responce)
            n = len(data)
            if h_type == 'group':
                limit = 3
            elif h_type == 'private':
                limit = 10
            if n > limit:
                n = limit
            msg = f'根据提供信息，已查询到{n}本关键词为[{h_msg}]的本子:'
            if h_type == 'group':
                msg = f'[CQ:at,qq={h_qq}]\n根据提供信息，已查询到{n}本关键词为[{h_msg}]的本子:'
            for i in range(n):
                msg0 = ('\n——————————\n本子链接：https://b-upp.com%s \n本子标题：%s '%(data[i]))
                msg += msg0
            await session.send(message=msg)