import re
import os
import json
import nonebot
from pathlib import Path
from random import randint, choice

from ATRI.modules.error import errorBack
from ATRI.modules.time import sleepTime
from ATRI.modules.funcControl import checkSwitch, checkNoob
from ATRI.plugins.SauceNAO import API_KEY, SauceNAO


bot = nonebot.get_bot()


@bot.on_message("group")
async def _(context):
    group = context["group_id"]
    user = context["user_id"]
    if sleepTime():
        pass
    else:
        if checkNoob(user, group):
            msg = str(context["message"])
            print(msg)
            if "搜图" in msg or "识图" in msg:
                if checkSwitch("saucenao_search", group):
                    try:
                        pattern = r"CQ:reply,id=(.*?)]"
                        info = re.findall(pattern, msg)
                        msgID = info[0]
                        print(msgID)
                    except:
                        print('ERROR-onMessage')
                        return

                    try:
                        with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'msgData.json', 'r') as f:
                            data = json.load(f)
                    except:
                        data = {}
                    
                    if msgID in data.keys():
                        msgR = data[f"{msgID}"]["msg"]

                        pattern = r"url=(.*?)]"
                        info = re.findall(pattern, msgR)
                        picURL = info[0]

                        try:
                            task = SauceNAO(api_key=API_KEY)
                            data = task.search(url=picURL)
                            msg0 = ''
                        except:
                            await bot.send_msg(group_id = group, message = errorBack('请求数据失败')) # type: ignore
                            return

                        print(data)
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
                            await bot.send_msg(group_id = group, message = errorBack('处理数据失败')) # type: ignore
                            return
                        if msg0:
                            if float(similarity) > 70:
                                await bot.send_msg(group_id = group, message = msg0) # type: ignore
                            else:
                                await bot.send_msg(group_id = group,  message = 'ATRI无法找到相似的图呢...') # type: ignore
                    
                else:
                    await bot.send_msg(group_id = group, message = '该功能已关闭...') # type: ignore
            
            else:
                try:
                    with open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'r') as f:
                        data = json.load(f)
                except:
                    data = {}

                if str(msg) in data.keys():
                    lt = data[f"{msg}"]
                    msg = lt[0]
                    prob = int(lt[1])
                    res = randint(1,prob)
                    if res == 1:
                        await bot.send_msg(
                            group_id = group,
                            message = msg
                        ) # type: ignore

@bot.on_message('group')
async def _(context):
    user = context["user_id"]
    group = context["group_id"]
    if checkNoob(user, group):
        if sleepTime():
            pass
        else:
            if randint(1,20) == 4:
                img = choice(
                    [
                        '11.jpg', '12.jpg', '23.jpg'
                    ]
                )
                img = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'emoji' / 'senren' / f'{img}')
                await bot.send_msg(message = f'[CQ:image,file=file:///{img}]', auto_escape = False) # type: ignore
            
            else:
                pass