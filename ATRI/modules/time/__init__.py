from random import choice
from datetime import datetime

def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now

def sleepTime():
    if 0 <= now_time() < 5.5:
        msg = choice(
            [
                'zzzz......',
                'zzzzzzzz......',
                'zzz...好涩哦..zzz....',
                '别...不要..zzz..那..zzz..',
                '嘻嘻..zzz..呐~..zzzz..'
            ]
        )
        return msg
    else:
        return False