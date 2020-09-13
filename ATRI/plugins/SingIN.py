import json
import datetime
from pathlib import Path
from random import randint
from nonebot import on_command, CommandSession

from ATRI.modules.time import sleepTime
from ATRI.modules.funcControl import checkNoob



# =========[好感度阶级说明]=========
#  - 0-100 陌生人
#  - 100-250 朋友
#  - 250-350 亲密的朋友
#  - 350-400 ???
#  - 400-* 开冲
# =================================



@on_command('SingIN', aliases = ['签到'])
async def _(session: CommandSession):
    group = session.event.group_id
    user = session.event.user_id
    if sleepTime():
        await session.send(sleepTime())
    else:
        if checkNoob(user, group):
            try:
                with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'r') as f:
                        data = json.load(f)
            except:
                data = {}

            try:
                if data[f"{user}"][1] == datetime.date.today().strftime('%y%m%d'):
                    await session.send('咱今天签到过啦~明天再来吧！')
                    return
            except:
                pass
            
            favoIMP = randint(1,5)

            try:
                with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'r') as f:
                    data = json.load(f)
                data[f"{user}"] = [f"{int(data[f'{user}'][0]) + favoIMP}", f"{datetime.date.today().strftime('%y%m%d')}"]
                with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'w') as f:
                    f.write(json.dumps(data))
                    f.close()
            except:
                data = {}
                data[f"{user}"] = [f"{favoIMP}", f"{datetime.date.today().strftime('%y%m%d')}"]
                with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'w') as f:
                    f.write(json.dumps(data))
                    f.close()

            IMP = int(data[f"{user}"][0])

            msg0 = f'[CQ:at,qq={user}]\n'
            msg0 += '签到成功ヾ(≧∇≦*)ゝ\n'
            msg0 += f'+ 好感度 {favoIMP}|{IMP}\n'

            if 0 <= IMP < 100:
                msg0 += '今日もいい日ですよ！~頑張ってください！'

            elif 100 <= IMP < 250:
                msg0 += 'アトリが心から応援します！'
            
            elif 250 <= IMP < 350:
                msg0 += 'アトリはあなたを待ちます'
            
            elif 350 <= IMP < 400:
                msg0 += 'わ...わたし...えと...す...'
            
            elif 400 <= IMP:
                msg0 += '好きだあなた好きだ！永遠！'
            
            await session.send(msg0)