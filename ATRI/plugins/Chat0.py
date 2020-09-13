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
from apscheduler.triggers.date import DateTrigger

import config
from ATRI.modules.favoIMP import AddFavoIMP, DelFavoIMP, GetFavoIMP
from ATRI.modules.time import now_time
from ATRI.modules.response import request_api
from ATRI.modules.funcControl import checkNoob


bot = nonebot.get_bot()
master = config.SUPERUSERS
KC_URL = 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn'


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
    group = session.event.group_id
    if checkNoob(user, group):
        if 5.5 <= now_time() < 9:
            res = randint(1,2)
            if res == 1:
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
            
            elif res == 2:
                voice = choice(
                    [
                        'ohayo1.amr', 'ohayo2.amr', 'ohayo3.amr', 'ohayo4.amr'
                    ]
                )
                voice = Path('.') / 'ATRI' / 'data' / 'voice' / f'{voice}'
                voice = os.path.abspath(voice)
                await session.send(f'[CQ:record,file=:///{voice}]')
        
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
    group = session.event.group_id
    if checkNoob(user, group):
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
    group = session.event.group_id
    if checkNoob(user, group):
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
            res = randint(1,2)
            if res == 1:
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
            
            elif res == 2:
                voice = Path('.') / 'ATRI' / 'data' / 'voice' / 'oyasuminasai.amr'
                voice = os.path.abspath(voice)
                await session.send(f'[CQ:record,file=:///{voice}]')
        
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
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            res = randint(1,3)
            if res == 1:
                # res = random.randint(1,10)
                img = choice(
                    [
                        'AZ.jpg', 'AZ1.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('suki', patterns = [r"喜欢|爱你|爱|suki|daisuki|すき|好き|贴贴|老婆|[Mm][Uu][Aa]|亲一个"])
async def az(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if 0 <= GetFavoIMP(user) < 250:
                img = choice(
                    [
                        'TZ.jpg', 'TZ1.jpg', 'TZ2.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')
            
            elif 250 <= GetFavoIMP(user):
                res = randint(1,2)
                if res == 1:
                    img = choice(
                        [
                            'SUKI.jpg', 'SUKI1.jpg', 'SUKI2.png'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')
            
                elif res == 2:
                    voice = choice(
                        [
                            'suki1.amr', 'suki2.amr'
                        ]
                    )
                    voice = Path('.') / 'ATRI' / 'data' / 'voice' / f'{voice}'
                    voice = os.path.abspath(voice)
                    await session.send(f'[CQ:record,file=file:///{voice}]')

@on_command('kouchou', patterns = [r"草你妈|操|你妈|脑瘫|废柴|fw|five|废物|战斗|爬|爪巴|sb|SB|啥[b批比逼]|傻b|给[爷👴]爬|嘴臭"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                DelFavoIMP(u, 5, True)
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
                        voice = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'voice' / 'ATR_b402_027.amr')
                        await session.send(f'[CQ:record,file=file:///{voice}]')
                    
                    elif res == 2:
                        await session.send('鱼雷组合拳——————————————————啊————！！！')
                        voice = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'voice' / 'CombinationTorpedoFist.amr')
                        await session.send(f'[CQ:record,file=file:///{voice}]')
                    
                    elif res == 3:
                        await session.send('火箭拳——————————————————————————！！！')
                        voice = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'voice' / 'RocketPunch.amr')
                        await session.send(f'[CQ:record,file=file:///{voice}]')
                
                elif res == 3:
                    await session.send(request_api(KC_URL))

@on_command('ciallo', patterns = [r"[Cc][iI][aA][lL][lL][oO]"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
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
    group = session.event.group_id
    if checkNoob(user, group):
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
    group = session.event.group_id
    if checkNoob(user, group):
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
            
            elif randint(1,2) == 2:
                voice = choice(
                    [
                        'PX1.amr', 'PX2.amr', 'PX3.amr', 'PX4.amr', 'PX5.amr', 'PX6.amr'
                    ]
                )
                voice = Path('.') / 'ATRI' / 'data' / 'voice' / f'{voice}'
                voice = os.path.abspath(voice)
                await session.send(f'[CQ:record,file=file:///{voice}]')

@on_command('qingjie', patterns = [r"青[洁结]"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
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
    group = session.event.group_id
    if checkNoob(user, group):
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
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / 'H.jpg'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('high_per', patterns = [r"高性能|[太最][棒好强猛]|[tT][qQ][lL]|[🐂牛nN][🍺批bB]|すごい|sugoi|[斯死]国一|よかった"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    msg = str(session.event.message)
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            pat = r"草你妈|操|你妈|脑瘫|废柴|fw|five|废物|战斗|爬|爪巴|sb|SB|啥[b批比逼]|傻b|给[爷👴]爬|嘴臭"
            if re.findall(pat, msg):
                pass
            else:
                AddFavoIMP(user, 3, True)
                msg = choice(
                    [
                       '当然，我是高性能的嘛~！',
                       '小事一桩，我是高性能的嘛',
                       '怎么样？还是我比较高性能吧？',
                       '哼哼！我果然是高性能的呢！',
                       '因为我是高性能的嘛！嗯哼！',
                       '因为我是高性能的呢！',
                       '哎呀~，我可真是太高性能了',
                       '正是，因为我是高性能的',
                       '是的。我是高性能的嘛♪',
                       '毕竟我可是高性能的！',
                       '嘿嘿，我的高性能发挥出来啦♪',
                       '我果然是很高性能的机器人吧！',
                       '是吧！谁叫我这么高性能呢！哼哼！',
                       '交给我吧，有高性能的我陪着呢',
                       '呣......我的高性能，毫无遗憾地施展出来了......'
                    ]
                )
                await session.send(msg)

@on_command('dont_worry', patterns = [r"没事|没关系|大丈夫|还好|不要紧|没出大问题|没伤到哪"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    msg = str(session.event.message)
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            pat = r"草你妈|操|你妈|脑瘫|废柴|fw|five|废物|战斗|爬|爪巴|sb|SB|啥[b批比逼]|傻b|给[爷👴]爬|嘴臭"
            if re.findall(pat, msg):
                pass
            else:
                msg = choice(
                    [
                       '当然，我是高性能的嘛~！',
                       '没事没事，因为我是高性能的嘛！嗯哼！',
                       '没事的，因为我是高性能的呢！',
                       '正是，因为我是高性能的',
                       '是的。我是高性能的嘛♪',
                       '毕竟我可是高性能的！',
                       '那种程度的事不算什么的。\n别看我这样，我可是高性能的',
                       '没问题的，我可是高性能的'
                    ]
                )
                await session.send(msg)

@on_command('mohead', patterns = [r"摸[头摸]"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    msg = str(session.event.message)
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            pat = r"草你妈|操|你妈|脑瘫|废柴|fw|five|废物|战斗|爬|爪巴|sb|SB|啥[b批比逼]|傻b|给[爷👴]爬|嘴臭"
            if re.findall(pat, msg):
                pass
            else:
                res = randint(1,3)
                if 1 <= res <= 2:
                    img = choice(
                        [
                            'TZ.jpg', 'TZ1.jpg', 'TZ2.jpg'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')
                
                elif res == 3:
                    AddFavoIMP(user, 1, False)
                    msg = choice(
                        [
                            '头发的柔顺度上升，我的高性能更上一层楼......',
                            '*蹭蹭'
                        ]
                    )
                    await session.send(msg)

@on_command('whl', patterns = [r"我好了|[wW][hH[lL]"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                await session.send('不许好！憋回去！')

@on_command('birthday', patterns = [r"生日快乐|生快|[bB]irthday|誕生日|tanjobi"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if datetime.date.today().strftime('%y%m%d') == '200828':
                AddFavoIMP(user, 50, True)
                res = randint(1,3)
                if res == 1:
                    msg = choice(
                        [
                            '谢谢，谢谢你！',
                            '感谢...15551',
                            '谢谢你们orz...'
                        ]
                    )
                    await session.send(msg)
                
                elif 2 <= res <= 3:
                    voice = choice(
                        [
                            'THX.amr', 'THX1.amr', 'THX2.amr', 'THX3.amr', 'THX4.amr'
                        ]
                    )
                    voice = Path('.') / 'ATRI' / 'data' / 'voice' / f'{voice}'
                    voice = os.path.abspath(voice)
                    await session.send(f'[CQ:record,file=file:///{voice}]')

                if randint(1,3) == 2:
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / 'SUKI.jpg'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')

            else:
                pass


@on_command('nicesleep', patterns = [r"精致睡眠"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if user == master:
            await session.send('那...请主人自己闭上眼！哼唧')
            return
        else:
            await session.send('恭喜！您已被ATRI屏蔽7小时')
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json', 'r') as f:
                    bL = json.load(f)
            except:
                bL = {}
            bL[f"{user}"] = f"{user}"
            file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
            f = open(file, 'w')
            f.write(json.dumps(bL))
            f.close()
            delta = timedelta(hours = 7)
            trigger = DateTrigger(
                run_date = datetime.now() + delta
            )

            scheduler.add_job( #type: ignore
                func = rmQQfromNoobLIST,
                trigger = trigger,
                args = (session.event.user_id,),
                misfire_grace_time = 60,
            )

noobList0 = []
@on_command('robozi', patterns = [r"萝卜子"], only_to_me = False)
async def _(session: CommandSession):
    global noobList0
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json', 'r') as f:
                    bL = json.load(f)
            except:
                bL = {}
            noobList0.append(user)
            if countX(noobList0, user) == 1:
                await session.send('萝卜子是对机器人的蔑称！')

            elif countX(noobList0, user) == 2:
                if user == master:
                    await session.send('是主人的话...那算了...呜呜\n即使到达了ATRI的最低忍耐限度......')
                    noobList0 = list(set(noobList0))
                    pass

                else:
                    await session.send('是亚托莉......萝卜子可是对机器人的蔑称......\n这是第二次警告哦，接下来10分钟我不会再理你了！哼唧！\n（好感度-1）')
                    DelFavoIMP(user, 1, False)
                    bL[f"{user}"] = f"{user}"
                    file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
                    f = open(file, 'w')
                    f.write(json.dumps(bL))
                    f.close()
                    noobList0 = list(set(noobList0))
                    print(noobList0)
                    delta = timedelta(minutes = 10)
                    trigger = DateTrigger(
                        run_date = datetime.now() + delta
                    )

                    scheduler.add_job( #type: ignore
                        func = rmQQfromNoobLIST,
                        trigger = trigger,
                        args = (session.event.user_id,),
                        misfire_grace_time = 60,
                    )

noobList1 = []
@on_command('ntr', patterns = [r"[nNηиɴИ][tT][rR]|[牛🐂🐮]头人"], only_to_me = False)
async def _(session: CommandSession):
    global noobList1
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            msg = str(session.event.message)
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json', 'r') as f:
                    bL = json.load(f)
            except:
                bL = {}
            pattern = r"[nNηиɴИ][tT][rR]|[牛🐂🐮]头人"
            if re.findall(pattern, msg):
                noobList1.append(user)
                if countX(noobList1, user) == 5:
                    if user == master:
                        await session.send('是主人的话...那算了...呜呜\n即使到达了ATRI的最低忍耐限度......')
                        noobList1 = list(set(noobList1))
                        pass

                    else:
                        await session.send(f'[CQ:at,qq={user}]哼！接下来30分钟别想让我理你！\n（好感度-2）')
                        DelFavoIMP(user, 2, False)
                        bL[f"{user}"] = f"{user}"
                        file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
                        f = open(file, 'w')
                        f.write(json.dumps(bL))
                        f.close()
                        noobList1 = list(set(noobList1))
                        print(noobList1)
                        delta = timedelta(minutes = 30)
                        trigger = DateTrigger(
                            run_date = datetime.now() + delta
                        )

                        scheduler.add_job( #type: ignore
                            func = rmQQfromNoobLIST,
                            trigger = trigger,
                            args = (session.event.user_id,),
                            misfire_grace_time = 60,
                        )
                
                else:
                    await session.send('你妈的，牛头人，' + request_api(KC_URL))