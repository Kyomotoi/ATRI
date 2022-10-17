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

from ATRI.log import log
from ATRI.service import Service
from ATRI.permission import ADMIN
from ATRI.message import MessageBuilder
from ATRI.plugins.rss.rss_rsshub.data_source import RssHubSubscriptor
from ATRI.utils import timestamp2datetime
from ATRI.utils.apscheduler import scheduler
from ATRI.database import RssMikananiSubcription

from .data_source import RssMikananSubscriptor


plugin = (
    Service("rss.mikan")
    .document("Rss的mikan支持")
    .permission(ADMIN)
    .main_cmd("/rss.mikan")
)
sub = RssMikananSubscriptor()


add_sub = plugin.cmd_as_group("add", "为本群添加 Mikan 订阅")


@add_sub.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("rm_add_url", args)


@add_sub.got("rm_add_url", prompt="Mikan 链接呢? 速速")
async def _(event: GroupMessageEvent, _url: str = ArgPlainText("rm_add_url")):
    group_id = event.group_id

    result = await sub.add_sub(_url, group_id)
    await add_sub.finish(result)


del_sub = plugin.cmd_as_group("del", "删除本群 Mikan 订阅")


@del_sub.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id

    query_result = await sub.get_sub_list({"group_id": group_id})
    if not query_result:
        await del_sub.finish("本群还没有任何订阅呢...")

    subs = list()
    for i in query_result:
        subs.append([i._id, i.title])

    output = "本群的 Mikan 订阅列表如下~\n" + tabulate(
        subs, headers=["ID", "Title"], tablefmt="plain"
    )
    await del_sub.send(output)


@del_sub.got("rm_del_sub_id", prompt="要取消的ID呢? 速速\n(键入 q 以取消)")
async def _(event: GroupMessageEvent, _id: str = ArgPlainText("rm_del_sub_id")):
    if _id == "q":
        await del_sub.finish("已取消操作~")

    group_id = event.group_id

    result = await sub.del_sub(_id, group_id)
    await del_sub.finish(result)


get_sub_list = plugin.cmd_as_group("list", "获取本群 Mikan 订阅列表", permission=Permission())


@get_sub_list.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id

    query_result = await sub.get_sub_list({"group_id": group_id})
    if not query_result:
        await get_sub_list.finish("本群还没有任何订阅呢...")

    subs = list()
    for i in query_result:
        subs.append([i.update_time, i.title])

    output = "本群的 Mikan 订阅列表如下~\n" + tabulate(
        subs, headers=["最后更新时间", "标题"], tablefmt="plain"
    )
    await get_sub_list.finish(output)


tq = asyncio.Queue()


class RssMikanDynamicChecker(BaseTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        conf = plugin.load_service("rss.mikan")
        if conf.get("enabled"):
            return now


@scheduler.scheduled_job(
    AndTrigger([IntervalTrigger(seconds=60), RssMikanDynamicChecker()]),
    name="Mikan 订阅检查",
    max_instances=3,  # type: ignore
    misfire_grace_time=60,  # type: ignore
)
async def _():
    try:
        all_dy = await sub.get_all_subs()
    except Exception:
        log.debug("Mikan 订阅列表为空 跳过")
        return

    if tq.empty():
        for i in all_dy:
            await tq.put(i)
    else:
        data: RssMikananiSubcription = tq.get_nowait()
        log.info(f"准备查询 Mikan: {data.title} 的动态, 队列剩余 {tq.qsize()}")

        raw_ts = data.update_time.replace(
            tzinfo=pytz.timezone("Asia/Shanghai")
        ) + timedelta(hours=8)
        ts = raw_ts.timestamp()

        info = await sub.get_mikan_info(data.rss_link)
        if not info:
            log.warning(f"无法获取 Mikan: {data.rss_link} 的动态")
            return

        time_patt = "%Y-%m-%dT%H:%M:%S.%f"

        if len(info) == 1:
            pub_date = info["item"]["torrent"]["pubDate"]
            link = info["item"]["torrent"]["link"]
        else:
            item = info["item"][0]

            pub_date = item["torrent"]["pubDate"]
            link = item["torrent"]["link"]

        m_t = datetime.strptime(pub_date, time_patt).timestamp()

        if ts < m_t:
            title = data.title

            repo = MessageBuilder("本群订阅的 Mikan 更新啦!").text(f"{title}").text(f"{link}")

            bot = get_bot()
            await bot.send_group_msg(group_id=data.group_id, message=repo)
            await sub.update_sub(
                data._id, data.group_id, {"update_time": timestamp2datetime(m_t)}
            )
