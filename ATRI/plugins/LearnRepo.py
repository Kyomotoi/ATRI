import json
from datetime import datetime
from pathlib import Path
import nonebot
from nonebot import on_command
from nonebot import CommandSession

import config
from ATRI.modules.error import errorBack


bot = nonebot.get_bot()
master = config.SUPERUSERS
__plugin_name__ = "LearnRepo"

def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


@on_command('add_word', aliases = ['增加词汇', '删除词汇', '学习词汇'], only_to_me = False)
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

        if w_tpye == '增加词汇' or w_tpye == '学习词汇':
            repo = msg[2]
            prob = int(msg[3])
            if word in data.keys():
                await session.send('该词已存在~！')

            else:
                try:
                    data[f"{word}"] = [f"{repo}",prob]
                    f = open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'w')
                    f.write(json.dumps(data))
                    f.close()
                    session.finish(f"学習しました！\nWord：[{word}]\nRepo：[{repo}]\nProbability：[{'%.2f%%' % (round(1 / prob , 1) * 100)}]")
                except:
                    session.finish(errorBack('写入失败'))

        elif w_tpye == '删除词汇':
            if word in data.keys():
                try:
                    data.pop(f"{word}")
                    f = open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'w')
                    f.write(json.dumps(data))
                    f.close()
                    await session.send(f'已成功从ATRI记忆模块中抹除[{word}]')
                except:
                    session.finish(errorBack('移除失败'))
            
            else:
                 session.finish(f'ATRI貌似没法从记忆中找到关键词[{word}]呢...')