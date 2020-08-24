import json
from random import randint
from datetime import datetime
from pathlib import Path
import nonebot
from nonebot import on_command
from nonebot import CommandSession

import config # type: ignore
from ATRI.modules.funcControl import checkNoob # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()
__plugin_name__ = "LearnRepo"

def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


@on_command('add_word', aliases = ['增加词汇', '删除词汇'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id == master:
        msg = session.event.raw_message.split(' ', 3)
        w_tpye = msg[0]
        word = msg[1]
        try:
            with open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'r') as f:
                data = json.load(f)
        except:
            data = {}

        if w_tpye == '增加词汇':
            repo = msg[2]
            prob = int(msg[3])
            if word in data.keys():
                await session.send('该词已存在~！')

            else:
                data[f"{word}"] = [f"{repo}",prob]
                f = open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'w')
                f.write(json.dumps(data))
                f.close()
                session.finish(f"学習しました！\nWord：[{word}]\nRepo：[{repo}]\nProbability：[{'%.2f%%' % (round(1 / prob , 1) * 100)}]")
        
        elif w_tpye == '删除词汇':
            if word in data.keys():
                data.pop(word)
                await session.send(f'已成功从ATRI记忆模块中抹除[{word}]')
            
            else:
                 session.finish(f'ATRI貌似没法从记忆中找到关键词[{word}]呢...')


@bot.on_message("group")
async def repo(context):
    user = context["user_id"]
    group = context["group_id"]
    word = context["message"]
    if 0 <= now_time() < 5.5:
        pass
    else:
        if checkNoob(user, group):
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'r') as f:
                    data = json.load(f)
            except:
                data = {}

            if str(word) in data.keys():
                lt = data[f"{word}"]
                msg = lt[0]
                prob = int(lt[1])
                res = randint(1,prob)
                if res == 1:
                    await bot.send_msg(
                        group_id = group,
                        message = msg
                    ) # type: ignore