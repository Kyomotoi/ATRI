import os
import json
import nonebot
from pathlib import Path


bot = nonebot.get_bot()


@bot.on_message('group')
async def _(ctx):
    group = ctx['group_id']
    user = ctx['user_id']
    msgID = ctx['message_id']
    RAWmsg = ctx['message']

    try:
        with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'msgData.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    data[f'{msgID}'] = {"msg": f"{RAWmsg}", "user_id": f"{user}"}

    try:
        with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'msgData.json', 'w') as f:
            f.write(json.dumps(data))
            f.close()
    except:
        os.mkdir(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}')
        with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'msgData.json', 'w') as f:
            f.write(json.dumps(data))
            f.close()