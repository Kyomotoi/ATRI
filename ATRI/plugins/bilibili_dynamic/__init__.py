import re
import pytz
import asyncio
from tabulate import tabulate
from datetime import datetime, timedelta

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger

from nonebot import get_bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent

from ATRI.log import logger as log
from ATRI.utils import timestamp2datetime
from ATRI.utils.apscheduler import scheduler

from .data_source import BilibiliDynamicSubscriptor
from .database.models import Subscription


add_sub = BilibiliDynamicSubscriptor().cmd_as_group("add", "添加b站up主订阅")


@add_sub.handle()
async def _bd_add_sub(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("bd_add_sub_id", args)


@add_sub.got("bd_add_sub_id", "up主id呢？速速")
async def _bd_deal_add_sub(
    event: GroupMessageEvent, _id: str = ArgPlainText("bd_add_sub_id")
):
    patt = r"^\d+$"
    if not re.match(patt, _id):
        await add_sub.reject("这似乎不是id呢，请重新输入:")

    __id = int(_id)
    group_id = event.group_id
    sub = BilibiliDynamicSubscriptor()

    up_nickname = await sub.get_up_nickname(__id)
    if not up_nickname:
        await add_sub.finish(f"无法获取id为 {_id} 的up主信息...操作失败了")

    query_result = await sub.get_sub_list(__id, group_id)
    if len(query_result):
        await add_sub.finish(f"该up主[{up_nickname}]已在本群订阅列表中啦！")

    await sub.add_sub(__id, group_id)
    await sub.update_sub(
        __id, {"up_nickname": up_nickname, "last_update": datetime.utcnow()}
    )
    await add_sub.finish(f"成功订阅名为[{up_nickname}]up主的动态～！")


del_sub = BilibiliDynamicSubscriptor().cmd_as_group("del", "删除b站up主订阅")


@del_sub.handle()
async def _bd_del_sub(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("bd_del_sub_id", args)


@del_sub.got("bd_del_sub_id", "up主id呢？速速")
async def _bd_deal_del_sub(
    event: GroupMessageEvent, _id: str = ArgPlainText("bd_del_sub_id")
):
    patt = r"^\d+$"
    if not re.match(patt, _id):
        await add_sub.reject("这似乎不是id呢，请重新输入:")

    __id = int(_id)
    group_id = event.group_id
    sub = BilibiliDynamicSubscriptor()

    up_nickname = await sub.get_up_nickname(__id)
    if not up_nickname:
        await add_sub.finish(f"无法获取id为 {__id} 的up主信息...操作失败了")

    query_result = await sub.get_sub_list(__id, group_id)
    if not query_result:
        await del_sub.finish(f"取消订阅失败...该up主[{up_nickname}]并不在本群订阅列表中")

    await sub.del_sub(__id, group_id)
    await del_sub.finish(f"成功取消该up主[{up_nickname}]的订阅～")


get_sub_list = BilibiliDynamicSubscriptor().cmd_as_group("list", "获取b站up主订阅列表")


@get_sub_list.handle()
async def _get_sub_list(event: GroupMessageEvent):
    group_id = event.group_id
    sub = BilibiliDynamicSubscriptor()

    query_result = await sub.get_sub_list(group_id=group_id)
    if not query_result:
        await get_sub_list.finish("本群还未订阅任何up主呢...")

    subs = list()
    for i in query_result:
        tm = i.last_update.replace(tzinfo=pytz.timezone("Asia/Shanghai"))
        subs.append([i.up_nickname, i.uid, tm + timedelta(hours=8)])

    output = "本群订阅的up列表如下～\n" + tabulate(
        subs, headers=["up主", "uid", "最后更新时间"], tablefmt="plain", showindex=True
    )
    await get_sub_list.finish(output)


tq = asyncio.Queue()


class BilibiliDynamicChecker(BaseTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        sub = BilibiliDynamicSubscriptor()
        conf = sub.load_service("b站动态订阅-rebu")
        if conf.get("enabled"):
            return now


@scheduler.scheduled_job(
    AndTrigger([IntervalTrigger(seconds=10), BilibiliDynamicChecker()]),
    name="b站动态更新检查",
    max_instances=3,  # type: ignore
    misfire_grace_time=60,  # type: ignore
)
async def _check_dynamic():
    sub = BilibiliDynamicSubscriptor()
    all_dy = await sub.get_all_subs()
    if tq.empty():
        for i in all_dy:
            await tq.put(i)
    else:
        m: Subscription = tq.get_nowait()
        log.info(f"准备查询up主[{m.up_nickname}]的动态，队列剩余 {tq.qsize()}")

        ts = int(m.last_update.timestamp())
        info: dict = await sub.get_up_recent_dynamic(m.uid)
        result = list()
        if info.get("cards", list()):
            result = sub.extract_dyanmic(info["cards"])
        if not result:
            log.warning(f"无法获取up主[{m.up_nickname}]的动态")

        for i in result:
            i["name"] = m.up_nickname
            if ts < i["timestamp"]:
                content = Message(sub.gen_output(i))

                bot = get_bot()
                await bot.send_group_msg(group_id=m.group_id, message=content)
                await sub.update_sub(
                    m.uid,
                    {
                        "group_id": m.group_id,
                        "last_update": timestamp2datetime(i["timestamp"]),
                    },
                )
                break
