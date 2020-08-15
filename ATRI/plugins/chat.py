import os
import re
import json
import nonebot
import warnings
from pathlib import Path
from random import randint, choice
from datetime import datetime, timedelta
from nonebot import on_command, scheduler
from nonebot import CommandSession
from nonebot import on_command
from apscheduler.triggers.date import DateTrigger

from ATRI.modules import response # type: ignore
import config # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()
KC_URL = 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn'


@nonebot.scheduler.scheduled_job(
    'cron',
    day_of_week = "mon,tue,wed,thu,fri,sat,sun",
    hour = 7
)
async def _():
    """早安"""
    try:
        group_list = await bot.get_group_list() #type: ignore
        groups = [group['group_id'] for group in group_list]
        res = randint(1,2)
        if res == 1:
            msg = choice(
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
                    '......(打瞌睡)',
                ]
            )
        
        elif res == 2:
            img = Path('.') / 'ATRI' / 'data' / 'emoji' / 'SY.jpg'
            img = os.path.abspath(img)
            msg = f'[CQ:image,file=file:///{os.path.abspath(img)}]'

        for group in groups:
            await bot.send_group_msg(group_id = group, message = msg) #type: ignore
    
    except:
        pass

@nonebot.scheduler.scheduled_job(
    'cron',
    day_of_week = "mon,tue,wed,thu,fri,sat,sun",
    hour = 22
)
async def _():
    """晚安"""
    try:
        group_list = await bot.get_group_list() #type: ignore
        groups = [group['group_id'] for group in group_list]
        res = randint(1,2)
        if res == 1:
            msg = choice(
                [
                    '忙累了一天，快休息吧',
                    '辛苦了一天，准备睡觉吧',
                    '一起睡觉吧~~~~~',
                    '......该睡觉了',
                    '还不睡等着猝死？嗯！？'

                ]
            )

        elif res == 2:
            img = choice(
                [
                    'SJ.jpg', 'SJ1.jpg'
                ]
            )
            img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
            img = os.path.abspath(img)
            msg = f'[CQ:image,file=file:///{os.path.abspath(img)}]'

        for group in groups:
            await bot.send_group_msg(group_id = group, message = msg) #type: ignore

    except:
        pass


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now

def countX(lst, x):
    warnings.simplefilter('ignore', ResourceWarning)
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count

def rmQQfromNoobLIST(user):
    file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
    with open(file, 'r') as f:
        bL = json.load(f)
    bL.pop(f"{user}")
    f = open(file, 'w')
    f.write(json.dumps(bL))
    f.close()


@on_command('morning', patterns = [r"早[安哇]|早上好|ohayo|哦哈哟|お早う"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 5.5 <= now_time() < 9:
            await session.send(
                choice(
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
            await session.send(
                choice(
                    [
                        '哼！这个点还早啥，昨晚干啥去了！？',
                        '熬夜了对吧熬夜了对吧熬夜了对吧？？？！',
                        '是不是熬夜是不是熬夜是不是熬夜？！'
                    ]
                )
            )
        
        elif 18 <= now_time() < 24:
            await session.send(
                choice(
                    [
                        '早个啥？哼唧！我都准备洗洗睡了！',
                        '不是...你看看几点了，哼！',
                        '晚上好哇'
                    ]
                )
            )
        
        elif 0 <= now_time() < 5.5:
            await session.send(
                choice(
                    [
                        'zzzz......',
                        'zzzzzzzz......',
                        'zzz...好涩哦..zzz....',
                        '别...不要..zzz..那..zzz..',
                        '嘻嘻..zzz..呐~..zzzz..',
                        '...zzz....哧溜哧溜....'
                    ]
                )
            )

@on_command('noon', patterns = [r"中午好|午安"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 11 <= now_time() <= 15:
            await session.send(
                choice(
                    [
                        '午安w','午觉要好好睡哦，ATRI会陪伴在你身旁的w',
                        '嗯哼哼~睡吧，就像平常一样安眠吧~o(≧▽≦)o',
                        '睡你午觉去！哼唧！！'
                    ]
                )
            )


@on_command('night', patterns = [r"晚安|oyasuminasai|おやすみなさい"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 5.5 <= now_time() < 11:
            await session.send(
                choice(
                    [
                        '你可猝死算了吧！',
                        '？啊这',
                        '亲，这边建议赶快去睡觉呢~~~',
                        '不可忍不可忍不可忍！！为何这还不猝死！！'
                    ]
                )
            )
        
        elif 11 <= now_time() < 15:
            await session.send(
                choice(
                    [
                        '午安w','午觉要好好睡哦，ATRI会陪伴在你身旁的w',
                        '嗯哼哼~睡吧，就像平常一样安眠吧~o(≧▽≦)o',
                        '睡你午觉去！哼唧！！'
                    ]
                )
            )
        
        elif 15 <= now_time() < 19:
            await session.send(
                choice(
                    [
                        '难不成？？晚上不想睡觉？？现在休息',
                        '就......挺离谱的...现在睡觉',
                        '现在还是白天哦，睡觉还太早了'
                    ]
                )
            )
        
        elif 19 <= now_time() < 24:
            await session.send(
                choice(
                    [
                        '嗯哼哼~睡吧，就像平常一样安眠吧~o(≧▽≦)o',
                        '......(打瞌睡)',
                        '呼...呼...已经睡着了哦~...呼......',
                        '......我、我会在这守着你的，请务必好好睡着'
                    ]
                )
            )
        
        elif 0 <= now_time() < 5.5:
            await session.send(
                choice(
                    [
                        'zzzz......',
                        'zzzzzzzz......',
                        'zzz...好涩哦..zzz....',
                        '别...不要..zzz..那..zzz..',
                        '嘻嘻..zzz..呐~..zzzz..'
                    ]
                )
            )


@on_command('az', patterns = [r"[aA][zZ]|[阿啊]这"], only_to_me = False)
async def az(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            res = randint(1,3)
            if res == 1:
                # res = random.randint(1,10)
                img = choice(
                    [
                        'AZ.jpg', 'AZ1.jpg', 'AZ2.jpg', 'AZ3.png', 'ZN.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('suki', patterns = [r"喜欢|爱你|爱|suki|daisuki|すき|好き|贴贴|老婆|[Mm][Uu][Aa]|亲一个"], only_to_me = True)
async def az(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            res = randint(1,3)
            if res == 1:
                # res = random.randint(1,10)
                img = choice(
                    [
                        'SUKI.jpg', 'SUKI1.jpg', 'SUKI2.png', 'HE1.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')
            
            elif 2 <= res <= 3:
                img = choice(
                    [
                        'TZ.jpg', 'TZ1.jpg', 'TZ2.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')


@on_command('wenhao', patterns = [r"'?'|？"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            res = randint(1,3)
            if res == 1:
                res = randint(1,5)
                if 1 <= res < 2:
                    await session.send(
                        choice(
                            [
                                '?', '？', '嗯？', '(。´・ω・)ん?', 'ん？'
                            ]
                        )
                    )
                
                elif 2 <= res <= 5:
                    img = choice(
                        [
                            'WH.jpg', 'WH1.jpg', 'WH2.jpg', 'WH3.jpg', 'WH4.jpg'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('yn', patterns = [r"是[吗]|是否"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,3) == 1:
                img = choice(
                    [
                        'YIQI_YES.png', 'YIQI_NO.jpg', 'KD.jpg', 'FD.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')



@on_command('kouchou', patterns = [r"草你妈|操|你妈|脑瘫|废柴|fw|five|废物|战斗|爬|爪巴|sb|SB|啥[b批比逼]|傻b|给[爷👴]爬|嘴臭"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                res = randint(1,3)
                if res == 1:
                    img = choice(
                        [
                            'WQ.jpg', 'WQ.png', 'WQ1.jpg', 'WQ2.jpg', 'FN.jpg'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')

                elif res == 2:
                    res = randint(1,3)
                    if res == 1:
                        await session.send('对嘴臭人以火箭组合必杀拳，来让他好好喝一壶！哼！')
                    
                    elif res == 2:
                        await session.send('鱼雷组合拳——————————————————啊————！！！')
                    
                    elif res == 3:
                        await session.send('火箭拳——————————————————————————！！！')
                
                elif res == 3:
                    await session.send(response.request_api(KC_URL))

@on_command('ciallo', patterns = [r"[Cc][iI][aA][lL][lL][oO]"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                res = randint(1,2)
                if res == 1:
                    img = choice(
                        [
                            'CIALLO.jpg', 'CIALLO1.jpg', 'CIALLO2.jpg', 'CIALLO3.jpg', 'CIALLO4.jpg', 'CIALLO5.jpg'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')
                
                elif res == 2:
                    await session.send('Ciallo～(∠・ω< )⌒★')

@on_command('ne', patterns = [r"呐|ねえ|口内"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,3) == 1:
                await session.send(
                    choice(
                        [
                            '呐', '呐呐呐', 'ねえ', 'ねえねえ'
                        ]
                    )
                )

@on_command('kani', patterns = [r"螃蟹|🦀|カニ|[kK]ani"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                img = choice(
                    [
                        'KN.png', 'KN.jpg', 'KN1.jpg', 'KN2.jpg', 'KN3.png'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('qingjie', patterns = [r"青[洁结]"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / 'H.jpg'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('jz', patterns = [r"就这"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                img = choice(
                    [
                        'JZ.png', 'JZ1.png'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('hai', patterns = [r"害|嗐"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / 'H.jpg'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

noobList = []
@on_command('ntr', patterns = [r"[nNηиɴИ][tT][rR]|[牛🐂]头人"], only_to_me = False)
async def _(session: CommandSession):
    global noobList
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if str(user) in data.keys():
        pass
    else:
        if 0 <= now_time() < 5.5:
            pass
        else:
            msg = str(session.event.message)
            bL = {}
            pattern = r"[nNηиɴИ][tT][rR]|[牛🐂]头人"
            if re.findall(pattern, msg):
                await session.send('你妈的，牛头人，' + response.request_api(KC_URL))
                noobList.append(user)
                print(noobList)
                print(countX(noobList, user))
                if countX(noobList, user) == 5:
                    if user == master:
                        await session.send('是主人的话...那算了...呜呜\n即使到达了ATRI的最低忍耐限度......')
                        noobList = list(set(noobList))
                        pass

                    else:
                        await session.send(f'[CQ:at,qq={user}]哼！接下来10分钟别想让我理你！')
                        bL[f"{user}"] = f"{user}"
                        file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
                        f = open(file, 'w')
                        f.write(json.dumps(bL))
                        f.close()
                        noobList = list(set(noobList))
                        print(noobList)
                        delta = timedelta(minutes = 10)
                        trigger = DateTrigger(
                            run_date = datetime.now() + delta
                        )

                        scheduler.add_job( #type: ignore
                            func = rmQQfromNoobLIST,
                            trigger = trigger,
                            args = (user),
                            misfire_grace_time = 60,
                        )

                else:
                    pass