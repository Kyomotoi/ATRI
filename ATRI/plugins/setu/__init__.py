import re
import asyncio
from random import choice
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.typing import T_State

from ATRI.config import BotSelfConfig
from ATRI.utils.limit import FreqLimiter, DailyLimiter
from ATRI.utils.apscheduler import scheduler
from .data_source import Setu


_setu_flmt = FreqLimiter(120)
_setu_dlmt = DailyLimiter(5)


random_setu = Setu().on_command(
    "来张涩图", "来张随机涩图，冷却2分钟，每天限5张", aliases={"涩图来", "来点涩图", "来份涩图"}
)


@random_setu.handle()
async def _random_setu(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _setu_flmt.check(user_id):
        await random_setu.finish()
    if not _setu_dlmt.check(user_id):
        await random_setu.finish()

    repo, setu = await Setu().random_setu()
    await bot.send(event, repo)

    msg_1 = dict()
    try:
        msg_1 = await bot.send(event, Message(setu))
    except Exception:
        await random_setu.finish("hso（发不出")

    event_id = msg_1["message_id"]
    _setu_flmt.start_cd(user_id)
    _setu_dlmt.increase(user_id)
    await asyncio.sleep(30)
    await bot.delete_msg(message_id=event_id)


tag_setu = Setu().on_regex(r"来[张点丶份](.*?)的[涩色🐍]图", "根据提供的tag查找涩图")


@tag_setu.handle()
async def _tag_setu(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _setu_flmt.check(user_id):
        await random_setu.finish()
    if not _setu_dlmt.check(user_id):
        await random_setu.finish()

    msg = str(event.message).strip()
    pattern = r"来[张点丶份](.*?)的[涩色🐍]图"
    tag = re.findall(pattern, msg)[0]
    repo, setu = await Setu().tag_setu(tag)
    if not setu:
        await tag_setu.finish(repo)

    await bot.send(event, repo)

    msg_1 = dict()
    try:
        msg_1 = await bot.send(event, Message(setu))
    except Exception:
        await random_setu.finish("hso（发不出")

    event_id = msg_1["message_id"]
    _setu_flmt.start_cd(user_id)
    _setu_dlmt.increase(user_id)
    await asyncio.sleep(30)
    await bot.delete_msg(message_id=event_id)


_catcher_max_file_size = 128


setu_catcher = Setu().on_message("涩图嗅探", block=False)


@setu_catcher.handle()
async def _setu_catcher(bot: Bot, event: MessageEvent):
    msg = str(event.message)
    pattern = r"url=(.*?)]"
    args = re.findall(pattern, msg)
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
            ss = "\n".join(ss)
            s_repo = f"多张涩图来咧！\n{ss}\n最涩的达到：{'{:.2%}'.format(hso[0])}"

        await bot.send(event, u_repo)
        for superuser in BotSelfConfig.superusers:
            await bot.send_private_msg(user_id=superuser, message=s_repo)


nsfw_checker = Setu().on_command("/nsfw", "涩值检测")


@nsfw_checker.handle()
async def _nsfw_checker(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["nsfw_img"] = msg


@nsfw_checker.got("nsfw_img", "图呢？")
async def _deal_check(bot: Bot, event: MessageEvent, state: T_State):
    msg = state["nsfw_img"]
    pattern = r"url=(.*?)]"
    args = re.findall(pattern, msg)
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


catcher_setting = Setu().on_command("嗅探", "涩图检测图片文件大小设置")


@catcher_setting.handle()
async def _catcher_setting(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["catcher_set"] = msg


@catcher_setting.got("catcher_set", "数值呢？（1对应1kb，默认128）")
async def _deal_setting(bot: Bot, event: MessageEvent, state: T_State):
    global _catcher_max_file_size
    msg = state["catcher_set"]
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
