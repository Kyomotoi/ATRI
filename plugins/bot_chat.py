import json
import random
from datetime import datetime
import time
from nonebot.helpers import render_expression
from pathlib import Path
from iotbot import GroupMsg
from iotbot import decorators as deco
from iotbot.sugar import Picture, Text, Voice


# 一些必要参数
bot_qq = 
comm_morning = ['早安','早上好', 'ohayo', '哦哈哟', 'お早う', '早']
comm_night = ['晚安', 'oyasuminasai', 'おやすみなさい']
voice_M_list =(
    'ohayo1.mp3',
    'ohayo2.mp3',
    'ohayo3.mp3',
    'ohayo4.mp3'
)

path_M = Path('.') / 'data' / 'voice' / f'{random.choice([voice_M_list])}'
path_N = Path('.') / 'data' / 'voice' / 'oyasuminasai.mp3'
path_pic = Path('.') / 'data' / 'emoji'


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


@deco.not_botself #早安 / 晚安
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.message['CurrentPacket']['Data']['Content']
    try:
        msg = json.loads(msg)
        if msg["UserID"] is bot_qq:
            pass
    except:
        pass

# ============================================= -> 早安
    if msg in comm_morning:

        if 5.5 <= now_time() < 9:
            res = random.randint(1,10)
            if 1 <= res <= 6:
                Voice(voice_path = path_M)
                time.sleep(0.5)
                Picture(pic_path = str(path_pic) + 'HE.jpg')
            elif 6 < res <= 10:
                Text(
                    random.choice(
                        [
                            '啊......早上好...(哈欠)',
                            '唔......吧唧...早上...哈啊啊~~~\n早上好......',
                            '早上好......',
                            '早上好呜......呼啊啊~~~~',
                            '啊......早上好。\n昨晚也很激情呢！',
                            '吧唧吧唧......怎么了...已经早上了么...',
                            '早上好！',
                            '......看起来像是傍晚，其实已经早上了吗？',
                            '早上好......欸~~~脸好近呢'
                        ]
                    )
                )

        elif 9 <= now_time() < 18:
            Text(
                random.choice(
                    [
                        '哼！这个点还早啥，昨晚干啥去了！？',
                        '熬夜了对吧熬夜了对吧熬夜了对吧？？？！',
                        '是不是熬夜是不是熬夜是不是熬夜？！'
                    ]
                )
            )

        elif 18 <= now_time() < 24:
            Text(
                random.choice(
                    [
                        '早个啥？哼唧！我都准备洗洗睡了！',
                        '不是...你看看几点了，哼！',
                        '晚上好哇'
                    ]
                )
            )

        elif 0 <= now_time() < 5.5:
            Text(
                random.choice(
                    [
                        'zzzz......',
                        'zzzzzzzz......',
                        'zzz...好涩哦..zzz....',
                        '别...不要..zzz..那..zzz..',
                        '嘻嘻..zzz..呐~..zzzz..'
                    ]
                )
            )

# ============================================= -> 晚安
    elif msg in comm_night:
        
        if 5.5 <= now_time() < 11:
            res = random.randint(1,10)
            if 1 <= res <= 5:
                Picture(
                    pic_path = str(path_pic) + render_expression(
                        'AZ.jpg', 'ZN.jpg', 'ZZ.jpg'
                    )
                )
            elif 5< res <= 10:
                Text(
                    random.choice(
                        [
                            '你可猝死算了吧！',
                            '？啊这'
                        ]
                    )
                )
        
        elif 11 <= now_time() < 15:
            Text(
                random.choice(
                    [
                        '午安w','午觉要好好睡哦，ATRI会陪伴在你身旁的w',
                        '嗯哼哼~睡吧，就像平常一样安眠吧~o(≧▽≦)o'
                    ]
                )
            )
        
        elif 15 <= now_time() < 19:
            Text(
                random.choice(
                    [
                        '难不成？？晚上不想睡觉？？现在休息',
                        '就......挺离谱的...现在睡觉',
                        '现在还是白天哦，睡觉还太早了'
                    ]
                )
            )
        
        elif 19 <= now_time() < 24:
            res = random.randint(1,10)
            if 1 <= res <= 6:
                Voice(voice_path = path_N)
            elif 6 < res <= 10:
                Text(
                    random.choice(
                        [
                            '嗯哼哼~睡吧，就像平常一样安眠吧~o(≧▽≦)o',
                            '......(打瞌睡)',
                            '呼...呼...已经睡着了哦~...呼......',
                            '......我、我会在这守着你的，请务必好好睡着'
                        ]
                    )
                )

        elif 0 <= now_time() < 5.5:
            Text(
                random.choice(
                    [
                        'zzzz......',
                        'zzzzzzzz......',
                        'zzz...好涩哦..zzz....',
                        '别...不要..zzz..那..zzz..',
                        '嘻嘻..zzz..呐~..zzzz..'
                    ]
                )
            )
