import pytz
import asyncio
from tabulate import tabulate
from datetime import timedelta, datetime

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger

from nonebot import get_bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.permission import Permission
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent

from ATRI.log import logger as log
from ATRI.utils import timestamp2datetime
from ATRI.utils.apscheduler import scheduler
from ATRI.database import RssRsshubSubcription

from .data_source import RssHubSubscriptor


add_sub = RssHubSubscriptor().cmd_as_group("add", "为本群添加 RSSHub 订阅")


@add_sub.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("rrh_add_url", args)


@add_sub.got("rrh_add_url", "RSSHub 链接呢？速速")
async def _(event: GroupMessageEvent, _url: str = ArgPlainText("rrh_add_url")):
    group_id = event.group_id
    sub = RssHubSubscriptor()

    result = await sub.add_sub(_url, group_id)
    await add_sub.finish(result)


del_sub = RssHubSubscriptor().cmd_as_group("del", "删除本群 RSSHub 订阅")


@del_sub.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id
    sub = RssHubSubscriptor()

    query_result = await sub.get_sub_list({"group_id": group_id})
    if not query_result:
        await del_sub.finish("本群还没有任何订阅呢...")

    subs = list()
    for i in query_result:
        subs.append([i._id, i.title])

    output = "本群的 RSSHub 订阅列表如下～\n" + tabulate(
        subs, headers=["ID", "title"], tablefmt="plain"
    )
    await del_sub.send(output)


@del_sub.got("rrh_del_sub_id", "要取消的ID呢? 速速\n(键入 q 以取消)")
async def _(event: GroupMessageEvent, _id: str = ArgPlainText("rrh_del_sub_id")):
    if _id == "q":
        await del_sub.finish("已取消操作~")

    group_id = event.group_id
    sub = RssHubSubscriptor()

    result = await sub.del_sub(_id, group_id)
    await del_sub.finish(result)


get_sub_list = RssHubSubscriptor().cmd_as_group(
    "list", "获取本群 RSSHub 订阅列表", permission=Permission()
)


@get_sub_list.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id
    sub = RssHubSubscriptor()

    query_result = await sub.get_sub_list({"group_id": group_id})
    if not query_result:
        await get_sub_list.finish("本群还没有任何订阅呢...")

    subs = list()
    for i in query_result:
        subs.append([i.update_time, i.title])

    output = "本群的 RSSHub 订阅列表如下～\n" + tabulate(
        subs, headers=["最后更新时间", "标题"], tablefmt="plain"
    )
    await get_sub_list.send(output)


tq = asyncio.Queue()


class RssHubDynamicChecker(BaseTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        conf = RssHubSubscriptor().load_service("rss.rsshub")
        if conf["enabled"]:
            return now


@scheduler.scheduled_job(
    AndTrigger([IntervalTrigger(seconds=120), RssHubDynamicChecker()]),
    name="RssHub 订阅检查",
    max_instances=3,  # type: ignore
    misfire_grace_time=60,  # type: ignore
)
async def _():
    sub = RssHubSubscriptor()
    try:
        all_dy = await sub.get_all_subs()
    except Exception:
        log.debug("RssHub 订阅列表为空 跳过")
        return

    if tq.empty():
        for i in all_dy:
            await tq.put(i)
    else:
        m: RssRsshubSubcription = tq.get_nowait()
        log.info(f"准备查询 RssHub: {m.rss_link} 的动态, 队列剩余 {tq.qsize()}")

        raw_ts = m.update_time.replace(
            tzinfo=pytz.timezone("Asia/Shanghai")
        ) + timedelta(hours=8)
        ts = raw_ts.timestamp()

        info: dict = await sub.get_rsshub_info(m.rss_link)
        if not info:
            log.warning(f"无法获取 RssHub: {m.rss_link} 的动态")
            return

        t_time = info["item"][0]["pubDate"]
        time_patt = "%a, %d %b %Y %H:%M:%S GMT"

        raw_t = datetime.strptime(t_time, time_patt) + timedelta(hours=8)
        ts_t = raw_t.timestamp()

        if ts < ts_t:
            item = info["item"][0]
            title = item["title"]
            link = item["link"]

            repo = f"""本群订阅的 RssHub 更新啦！
            {title}
            {link}
            """

            bot = get_bot()
            await bot.send_group_msg(group_id=m.group_id, message=repo)
            await sub.update_sub(m._id, m.group_id, {"update_time": timestamp2datetime(ts_t)})
