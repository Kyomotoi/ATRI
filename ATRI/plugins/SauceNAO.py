import requests
import json
import re
from nonebot import on_command, CommandSession

import config
from ATRI.modules.error import errorBack
from ATRI.modules.time import sleepTime
from ATRI.modules.funcControl import checkSwitch, checkNoob


API_KEY = config.SauceNaoKEY
__plugin_name__ = "saucenao_search"


class SauceNAO:

    def __init__(self, api_key, output_type=2, testmode=0, dbmask=None, dbmaski=32768, db=5, numres=1):
        api = 'https://saucenao.com/search.php'
        self.api = api
        params = dict()
        params['api_key'] = api_key
        params['output_type'] = output_type
        params['testmode'] = testmode
        params['dbmask'] = dbmask
        params['dbmaski'] = dbmaski
        params['db'] = db
        params['numres'] = numres
        self.params = params

    def search(self, url):
        self.params['url'] = url
        res = requests.get(url=self.api,params=self.params)
        return res.content

@on_command('SauceNAO', aliases = ['以图识图', '以图搜图'], only_to_me = False)
async def SaucenaoSearch(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    msg = session.current_arg.strip()

    if checkNoob(user, group):
        if sleepTime():
            await session.send(sleepTime())
        else:
            if checkSwitch(__plugin_name__, group):
                if not msg:
                    msg = session.get('message', prompt="请发送一张图片")

                await session.send("开始以图识图")

                try:
                    p = '\\[CQ\\:image\\,file\\=.*?\\,url\\=(.*?)\\]'

                    img = re.findall(p, msg)

                    task = SauceNAO(api_key=API_KEY)
                    data = task.search(url=img)
                    msg0 = ''

                    try:
                        data = json.loads(data)['results'][0]
                        title = data['data']['title']
                        pixiv_id = data['data']['pixiv_id']
                        member_name = data['data']['member_name']
                        member_id = data['data']['member_id']
                        similarity = data['header']['similarity']
                        mini_url = data['header']['thumbnail']
                        msg0 = f'[CQ:at,qq={user}]'
                        msg0 += f'SauceNAO结果：'
                        msg0 += f'[CQ:image,file={mini_url}]\n'
                        msg0 += f'相似度：{similarity}%\n'
                        msg0 += f'标题：{title}\n'
                        msg0 += f'插画ID：{pixiv_id}\n'
                        msg0 += f'画师：{member_name}\n'
                        msg0 += f'画师ID：{member_id}\n'
                        msg0 += f'直链：https://pixiv.cat/{pixiv_id}.jpg'
                    except:
                        msg = '数据处理失败'

                    if float(similarity) > 70:
                        await session.send(msg0)
                    else:
                        await session.send("找不到相似的图呢...")

                except Exception:
                    session.finish(errorBack(msg))
            else:
                session.finish('该功能已关闭...')


@SaucenaoSearch.args_parser
async def _(session: CommandSession):
    if not session.is_first_run and session.current_arg.startswith('算了'):
        session.switch(session.current_arg[len('算了'):])
