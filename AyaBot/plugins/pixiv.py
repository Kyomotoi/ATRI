import json
import nonebot
import requests
from nonebot import on_command, CommandSession


@on_command('pixivsearch', aliases=['p站搜索'], only_to_me=False)
async def pixivsearch(session: CommandSession):
    gets = session.get('gets', prompt='请输入需要查询的pid码')
    try:
        URL = 'https://api.imjad.cn/pixiv/v1/?type=illust&id=' + gets
        print(URL)
        response = requests.request("GET", URL)
        html = response.text
        sr = json.loads(html)
        i = sr["response"][0]["id"]
        title = sr["response"][0]["title"]
        width = sr["response"][0]["width"]
        height = sr["response"][0]["height"]
        tags = sr["response"][0]["tags"]
        userid = sr["response"][0]["user"]["id"]
        account = sr["response"][0]["user"]["account"]
        name = sr["response"][0]["user"]["name"]
        await session.send(f'搜索结果如下:\nPid:{i}\nTitle:{title}\n宽高:{width}x{height}\nTags:{tags}\n作者id:{userid}\n账号名称:{account}\n名称:{name}')
    except:
        await session.send('连接似乎失败了呢...请稍后尝试')
   
@pixivsearch.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['gets'] = stripped_arg
        return
    
    if not stripped_arg:
        session.pause('请输入需要查询的pid码')
    session.state[session.current_key] = stripped_arg