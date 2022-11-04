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
from nonebot.permission import Permission
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent, Bot

from ATRI.log import log
from ATRI.service import Service
from ATRI.permission import ADMIN
from ATRI.utils import timestamp2datetime
from ATRI.utils.apscheduler import scheduler
from ATRI.permission import MASTER
from ATRI.database import TwitterSubscription

from .data_source import TwitterDynamicSubscriptor


__CONTENT_LIMIT = 0


sub = TwitterDynamicSubscriptor()


plugin = Service("推特动态订阅").document("推特动态订阅助手~").permission(ADMIN).main_cmd("/td")


add_sub = plugin.cmd_as_group("add", "添加推主订阅")


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

    result = await sub.add_sub(_name, group_id)
    await add_sub.finish(result)


del_sub = plugin.cmd_as_group("del", "删除推主订阅")


@del_sub.handle()
async def _td_del_sub(event: GroupMessageEvent):
    group_id = event.group_id

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

    result = await sub.del_sub(int(tid), group_id)
    await del_sub.finish(result)


get_sub_list = plugin.cmd_as_group("list", "获取本群推主订阅列表", permission=Permission())


@get_sub_list.handle()
async def _td_get_sub_list(event: GroupMessageEvent):
    group_id = event.group_id

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


limit_content = plugin.cmd_as_group("limit", "设置订阅内容字数限制", permission=MASTER)


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

    global __CONTENT_LIMIT
    __CONTENT_LIMIT = int(_limit)
    await limit_content.finish(f"成功！订阅内容展示将限制在 {__CONTENT_LIMIT} 以内！")


tq = asyncio.Queue()


class TwitterDynamicChecker(BaseTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        conf = plugin.load_service("推特动态订阅")
        if conf.get("enabled"):
            return now


@scheduler.scheduled_job(
    AndTrigger([IntervalTrigger(seconds=30), TwitterDynamicChecker()]),
    name="推特动态更新检查",
    max_instances=3,  # type: ignore
    misfire_grace_time=60,  # type: ignore
)
async def _check_td():
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

        try:
            _bot: Bot = get_bot()  # type: ignore
        except Exception:
            log.warning("当前无在线协议端, 已停止推送")
            return

        group_list = await _bot.get_group_list()
        gl = [f"{i['group_id']}" for i in group_list]
        if m.group_id not in gl:
            await sub.del_sub(m.tid, m.group_id)
            log.warning(f"群 {m.group_id} 不存在, 已删除订阅 {m.name}@{m.screen_name}")

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
            content = sub.gen_output(data, __CONTENT_LIMIT)

            try:
                await _bot.send_group_msg(group_id=m.group_id, message=content)
            except Exception:
                log.warning("推信息发送失败")

            await sub.update_sub(
                m.tid, m.group_id, {"last_update": timestamp2datetime(ts_t)}
            )
            if _pic:
                pic = Message(MessageSegment.image(_pic))
                try:
                    await _bot.send_group_msg(group_id=m.group_id, message=pic)
                except Exception:
                    log.warning("推图片发送失败")
