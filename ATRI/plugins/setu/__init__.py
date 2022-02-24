import re
import asyncio
from random import choice

from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls, Cooldown

from ATRI.config import BotSelfConfig
from ATRI.utils.apscheduler import scheduler
from .data_source import Setu


random_setu = Setu().on_command("来张涩图", "来张随机涩图，冷却2分钟", aliases={"涩图来", "来点涩图", "来份涩图"})


@random_setu.handle([Cooldown(120)])
async def _random_setu(bot: Bot, event: MessageEvent):
    loop = asyncio.get_running_loop()

    repo, setu = await Setu().random_setu()
    await bot.send(event, repo)

    try:
        msg_1 = await bot.send(event, Message(setu))
    except Exception:
        await random_setu.finish("hso（发不出")

    event_id = msg_1["message_id"]
    loop.create_task(Setu().async_recall(bot, event_id))


@random_setu.got("r_rush_after_think", prompt="看完不来点感想么-w-")
async def _(think: str = ArgPlainText("r_rush_after_think")):
    is_repo = will_think(think)
    if not is_repo:
        await random_setu.finish()
    else:
        await random_setu.finish(is_repo)


tag_setu = Setu().on_regex(r"来[张点丶份](.*?)的[涩色🐍]图", "根据提供的tag查找涩图，冷却2分钟")


@tag_setu.handle([Cooldown(120, prompt="慢...慢一..点❤")])
async def _tag_setu(bot: Bot, event: MessageEvent):
    loop = asyncio.get_running_loop()

    msg = str(event.get_message()).strip()
    pattern = r"来[张点丶份](.*?)的[涩色🐍]图"
    tag = re.findall(pattern, msg)[0]
    repo, setu = await Setu().tag_setu(tag)
    if not setu:
        await tag_setu.finish(repo)

    await bot.send(event, repo)

    try:
        msg_1 = await bot.send(event, Message(setu))
    except Exception:
        await random_setu.finish("hso（发不出")

    event_id = msg_1["message_id"]
    loop.create_task(Setu().async_recall(bot, event_id))


@tag_setu.got("t_rush_after_think", prompt="看完不来点感想么-w-")
async def _(think: str = ArgPlainText("t_rush_after_think")):
    is_repo = will_think(think)
    if not is_repo:
        await random_setu.finish()
    else:
        await random_setu.finish(is_repo)


_catcher_max_file_size = 128


setu_catcher = Setu().on_message("涩图嗅探", "涩图嗅探器", block=False)


@setu_catcher.handle()
async def _setu_catcher(bot: Bot, event: MessageEvent):
    args = extract_image_urls(event.message)
    if not args:
        return
    else:
        hso = list()
        for i in args:
            try:
                data = await Setu().detecter(i, _catcher_max_file_size)
            except Exception:
                return
            if data[1] > 0.7:
                hso.append(data[1])

        hso.sort(reverse=True)

        if not hso:
            return
        elif len(hso) == 1:
            u_repo = f"hso! 涩值：{'{:.2%}'.format(hso[0])}\n不行我要发给别人看"
            s_repo = (
                f"涩图来咧！\n{MessageSegment.image(args[0])}\n涩值：{'{:.2%}'.format(hso[0])}"
            )

        else:
            u_repo = f"hso! 最涩的达到：{'{:.2%}'.format(hso[0])}\n不行我一定要发给别人看"

            ss = list()
            for s in args:
                ss.append(MessageSegment.image(s))
            ss = "\n".join(map(str, ss))
            s_repo = f"多张涩图来咧！\n{ss}\n最涩的达到：{'{:.2%}'.format(hso[0])}"

        await bot.send(event, u_repo)
        for superuser in BotSelfConfig.superusers:
            await bot.send_private_msg(user_id=superuser, message=s_repo)


nsfw_checker = Setu().on_command("/nsfw", "涩值检测")


@nsfw_checker.got("nsfw_img", "图呢？")
async def _deal_check(bot: Bot, event: MessageEvent):
    args = extract_image_urls(event.message)
    if not args:
        await nsfw_checker.reject("请发送图片而不是其他东西！！")

    data = await Setu().detecter(args[0], _catcher_max_file_size)
    hso = data[1]
    if not hso:
        await nsfw_checker.finish("图太小了！不测！")

    resu = f"涩值：{'{:.2%}'.format(hso)}\n"
    if hso >= 0.75:
        resu += "hso！不行我要发给别人看"
        repo = f"涩图来咧！\n{MessageSegment.image(args[0])}\n涩值：{'{:.2%}'.format(hso)}"
        for superuser in BotSelfConfig.superusers:
            await bot.send_private_msg(user_id=superuser, message=repo)

    elif 0.75 > hso >= 0.5:
        resu += "嗯。可冲"
    else:
        resu += "还行8"

    await nsfw_checker.finish(resu)


catcher_setting = Setu().on_command("嗅探设置", "涩图检测图片文件大小设置", permission=SUPERUSER)


@catcher_setting.handle()
async def _catcher_setting(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("catcher_set", args)


@catcher_setting.got("catcher_set", "数值呢？（1对应1kb，默认128）")
async def _deal_setting(msg: str = ArgPlainText("catcher_set")):
    global _catcher_max_file_size
    try:
        _catcher_max_file_size = int(msg)
    except Exception:
        await catcher_setting.reject("请发送阿拉伯数字～！")

    repo = f"好诶！涩图检测文件最小值已设为：{_catcher_max_file_size}kb"
    await catcher_setting.finish(repo)


@scheduler.scheduled_job(
    "interval", name="涩批诱捕器", hours=1, misfire_grace_time=60, args=[Bot]
)
async def _scheduler_setu(bot):
    try:
        group_list = await bot.get_group_list()
        lucky_group = choice(group_list)
        group_id = lucky_group["group_id"]
        setu = await Setu().scheduler()
        if not setu:
            return

        msg_0 = await bot.send_group_msg(group_id=int(group_id), message=Message(setu))
        message_id = msg_0["message_id"]
        await asyncio.sleep(60)
        await bot.delete_msg(message_id=message_id)

    except Exception:
        pass


_ag_l = ["涩图来", "来点涩图", "来份涩图"]
_ag_patt = r"来[张点丶份](.*?)的[涩色🐍]图"

_nice_patt = r"[hH好][sS涩色][oO哦]|[嗯恩摁社蛇🐍射]了|(硬|石更)了|[牛🐂][牛🐂]要炸了|[炼恋]起来|开?导"
_nope_patt = r"不够[涩色]|就这|不行|不彳亍|一般|这也[是叫算]|[?？]|就这|爬|爪巴"
_again_patt = r"再来一张|不够"

_nice_repo = ["w", "好诶！", "ohh", "(///w///)", "🥵", "我也"]
_nope_repo = ["那你来发", "爱看不看", "你看不看吧", "看这种类型的涩图，是一件多么美妙的事情"]
_again_repo = ["没了...", "自己找去"]


def will_think(msg: str) -> str:
    if msg in _ag_l:
        return str()

    ag_jud = re.findall(_ag_patt, msg)
    if ag_jud:
        return str()

    nice_jud = re.findall(_nice_patt, msg)
    nope_jud = re.findall(_nope_patt, msg)
    again_jud = re.findall(_again_patt, msg)

    if nice_jud:
        return choice(_nice_repo)
    elif nope_jud:
        return choice(_nope_repo)
    elif again_jud:
        return choice(_again_repo)
    else:
        return str()
