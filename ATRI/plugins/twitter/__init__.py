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
from nonebot.permission import Permission, SUPERUSER
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent

from ATRI.log import logger as log
from ATRI.utils import timestamp2datetime
from ATRI.utils.apscheduler import scheduler
from ATRI.database import TwitterSubscription

from .data_source import TwitterDynamicSubscriptor


_CONTENT_LIMIT: int = 0


add_sub = TwitterDynamicSubscriptor().cmd_as_group("add", "添加推主订阅")


@add_sub.handle()
async def _td_add_sub(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("td_add_sub_name", args)


@add_sub.got("td_add_sub_name", "推主名呢？速速")
async def _td_deal_add_sub(
    event: GroupMessageEvent, _name: str = ArgPlainText("td_add_sub_name")
):
    group_id = event.group_id
    sub = TwitterDynamicSubscriptor()

    result = await sub.add_sub(_name, group_id)
    await add_sub.finish(result)


del_sub = TwitterDynamicSubscriptor().cmd_as_group("del", "删除推主订阅")


@del_sub.handle()
async def _td_del_sub(event: GroupMessageEvent):
    group_id = event.group_id
    sub = TwitterDynamicSubscriptor()

    query_result = await sub.get_sub_list(group_id=group_id)
    if not query_result:
        await del_sub.finish("本群还没有订阅任何推主呢...")

    subs = list()
    for i in query_result:
        subs.append([i.name, i.tid])

    output = "本群订阅的推主列表如下～\n" + tabulate(subs, headers=["推主名", "tid"], tablefmt="plain")
    await del_sub.send(output)


@del_sub.got("td_del_sub_tid", "要取消的tid呢？速速\n(键入 q 以取消)")
async def _td_deal_del_sub(
    event: GroupMessageEvent, _tid: str = ArgPlainText("td_del_sub_tid")
):
    patt = r"^\d+$"
    if not re.match(patt, _tid):
        await del_sub.reject("这似乎不是tid呢，请重新输入:")

    if _tid == "q":
        await del_sub.finish("已取消操作～")

    group_id = event.group_id
    tid = int(_tid)
    sub = TwitterDynamicSubscriptor()

    result = await sub.del_sub(int(tid), group_id)
    await del_sub.finish(result)


get_sub_list = TwitterDynamicSubscriptor().cmd_as_group(
    "list", "获取本群推主订阅列表", permission=Permission()
)


@get_sub_list.handle()
async def _td_get_sub_list(event: GroupMessageEvent):
    group_id = event.group_id
    sub = TwitterDynamicSubscriptor()

    query_result = await sub.get_sub_list(group_id=group_id)
    if not query_result:
        await get_sub_list.finish("本群还未订阅任何推主呢...")

    subs = list()
    for i in query_result:
        raw_tm = (
            i.last_update.replace(tzinfo=pytz.timezone("Asia/Shanghai"))
            + timedelta(hours=8, minutes=8)
        ).timestamp()
        tm = datetime.fromtimestamp(raw_tm).strftime("%m-%d %H:%M:%S")
        subs.append([i.name, tm])

    output = "本群订阅的推主列表如下～\n" + tabulate(
        subs, headers=["推主", "最后更新时间"], tablefmt="plain"
    )
    await get_sub_list.finish(output)


limit_content = TwitterDynamicSubscriptor().cmd_as_group(
    "limit", "设置订阅内容字数限制", permission=SUPERUSER
)


@limit_content.handle()
async def _td_get_limit(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("td_limit_int", args)


@limit_content.got("td_limit_int", "要限制内容在多少字以内呢？(默认200，0=不限制)")
async def _td_deal_limit(
    event: GroupMessageEvent, _limit: str = ArgPlainText("td_limit_int")
):
    patt = r"^\d+$"
    if not re.match(patt, _limit):
        await limit_content.reject("请键入阿拉伯数字:")

    global _CONTENT_LIMIT
    _CONTENT_LIMIT = int(_limit)
    await limit_content.finish(f"成功！订阅内容展示将限制在 {_CONTENT_LIMIT} 以内！")


tq = asyncio.Queue()


class TwitterDynamicChecker(BaseTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        sub = TwitterDynamicSubscriptor()
        conf = sub.load_service("推特动态订阅")
        if conf.get("enabled"):
            return now


@scheduler.scheduled_job(
    AndTrigger([IntervalTrigger(seconds=30), TwitterDynamicChecker()]),
    name="推特动态更新检查",
    max_instances=3,  # type: ignore
    misfire_grace_time=60,  # type: ignore
)
async def _check_td():
    sub = TwitterDynamicSubscriptor()
    try:
        all_dy = await sub.get_all_subs()
    except Exception:
        log.debug("推特订阅列表为空 跳过")
        return

    if tq.empty():
        for i in all_dy:
            await tq.put(i)
    else:
        m: TwitterSubscription = tq.get_nowait()
        log.info(f"准备查询推主 {m.name}@{m.screen_name} 的动态，队列剩余 {tq.qsize()}")

        raw_ts = m.last_update.replace(
            tzinfo=pytz.timezone("Asia/Shanghai")
        ) + timedelta(hours=8, minutes=8)
        ts = raw_ts.timestamp()

        info: dict = await sub.get_twitter_user_info(m.screen_name)
        if not info.get("status", list()):
            log.warning(f"无法获取推主 {m.name}@{m.screen_name} 的动态")
            return

        t_time = info["status"]["created_at"]
        time_patt = "%a %b %d %H:%M:%S +0000 %Y"

        raw_t = datetime.strptime(t_time, time_patt) + timedelta(hours=8)
        ts_t = raw_t.timestamp()

        if ts < ts_t:
            raw_media = info["status"]["entities"].get("media", dict())
            _pic = raw_media[0]["media_url"] if raw_media else str()

            data = {
                "name": info["name"],
                "content": info["status"]["text"],
            }
            content = sub.gen_output(data, _CONTENT_LIMIT)

            bot = get_bot()
            await bot.send_group_msg(group_id=m.group_id, message=content)
            await sub.update_sub(
                m.tid, m.group_id, {"last_update": timestamp2datetime(ts_t)}
            )
            if _pic:
                pic = Message(MessageSegment.image(_pic))
                try:
                    await bot.send_group_msg(group_id=m.group_id, message=pic)
                except Exception:
                    repo = "图片发送失败了..."
                    await bot.send_group_msg(group_id=m.group_id, message=repo)
