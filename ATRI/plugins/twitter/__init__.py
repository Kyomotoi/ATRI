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

    t_name, t_screen_name = await sub.get_twitter_username(_name)
    if not t_name or not t_screen_name:
        await add_sub.finish(f"无法获取名为 {_name} 的推主的信息...操作失败了")

    res = await sub.get_twitter_user_info(_name)
    tid = res["id"]

    query_result = await sub.get_sub_list(tid, group_id)
    if len(query_result):
        await add_sub.finish(f"该推主 {t_name}@{t_screen_name}\n已在本群订阅列表中啦！")

    await sub.add_sub(tid, group_id)
    await sub.update_sub(
        tid,
        group_id,
        {
            "name": t_name,
            "screen_name": t_screen_name,
            "last_update": datetime.utcnow(),
        },
    )
    await add_sub.finish(f"成功订阅名为 {t_name}@{t_screen_name} 推主的动态～！")


del_sub = TwitterDynamicSubscriptor().cmd_as_group("del", "删除推主订阅")


@del_sub.handle()
async def _td_del_sub(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("td_del_sub_name", args)


@del_sub.got("td_del_sub_name", "推主名呢？速速")
async def _td_deal_del_sub(
    event: GroupMessageEvent, _name: str = ArgPlainText("td_del_sub_name")
):
    group_id = event.group_id
    sub = TwitterDynamicSubscriptor()

    t_name, t_screen_name = await sub.get_twitter_username(_name)
    if not t_name or not t_screen_name:
        await add_sub.finish(f"无法获取名为 {_name} 的推主的信息...操作失败了")

    res = await sub.get_twitter_user_info(_name)
    tid = res["id"]

    query_result = await sub.get_sub_list(tid=tid, group_id=group_id)
    if not query_result:
        await del_sub.finish(f"取消订阅失败...该推主 {t_name}@{t_screen_name} 不在本群订阅列表中")

    await sub.del_sub(t_screen_name, group_id)
    await del_sub.finish(f"成功取消该推主 {t_name}@{t_screen_name} 的订阅～")


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
        tm = i.last_update.replace(tzinfo=pytz.timezone("Asia/Shanghai"))
        subs.append([i.name, i.tid, tm + timedelta(hours=8)])

    output = "本群订阅的推主列表如下～\n" + tabulate(
        subs, headers=["推主", "tid", "最后更新时间"], tablefmt="plain", showindex=True
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

        ts = m.last_update.timestamp()
        info: dict = await sub.get_twitter_user_info(m.screen_name)
        if not info.get("status", list()):
            log.warning(f"无法获取推主 {m.name}@{m.screen_name} 的动态")
            return

        tid = info["id"]

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
            if _pic:
                pic = Message(MessageSegment.image(_pic))
                try:
                    await bot.send_group_msg(group_id=m.group_id, message=pic)
                except Exception:
                    repo = "图片发送失败了..."
                    await bot.send_group_msg(group_id=m.group_id, message=repo)

            await sub.update_sub(tid, m.group_id, {"last_update": raw_t})
