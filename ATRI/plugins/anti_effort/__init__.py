import os
import re
import json
from random import choice

from nonebot import get_bot
from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    MessageSegment,
    GroupMessageEvent,
)
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.utils.apscheduler import scheduler

from .data_source import AntiEffort, PLUGIN_DIR


_lmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~", "呜呜...别急"])

_GET_URL_MSG = """请键入wakatime share embed URL:
获取方法:
  - 前往 wakatime.com/share/embed
  - Format 选择 JSON
  - Chart Type 选择 Coding Activity
  - Date Range 选择 Last 7 Days
  - 所需url就在下一栏 HTML 中的 url
""".strip()


add_user = AntiEffort().on_command("!我也要卷", "加入卷王统计榜")


@add_user.got(
    "waka_url",
    _GET_URL_MSG,
)
@add_user.got("rank_nickname", "如何在排行榜中称呼你捏")
@add_user.got("to_global", "你希望加入公共排行榜吗？(y/n)", [Cooldown(60, prompt=_lmt_notice)])
async def _deal_add_user(
    event: GroupMessageEvent,
    url: str = ArgPlainText("waka_url"),
    user_nickname: str = ArgPlainText("rank_nickname"),
    to_global: str = ArgPlainText("to_global"),
):
    group_id = event.group_id
    user_id = event.user_id
    aititude = ["y", "Y", "是", "希望", "同意"]
    if to_global in aititude:
        await AntiEffort().add_user(int(), user_id, user_nickname, url)

    result = await AntiEffort().add_user(group_id, user_id, user_nickname, url)
    await add_user.finish(result)


join_global_rank = AntiEffort().on_command("!参加公共卷", "加入公共卷王榜")


@join_global_rank.handle()
async def _join_global_rank(event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id

    raw_data = AntiEffort().get_data(group_id)
    if raw_data:
        data = raw_data["data"]
        for i in data:
            if i["user_id"] == user_id:
                user_nickname = i["user_nickname"]
                url = i["waka_url"]
                await AntiEffort().add_user(int(), user_id, user_nickname, url)
                await join_global_rank.finish("完成~！")


@join_global_rank.got("waka_url", _GET_URL_MSG)
@join_global_rank.got(
    "rank_nickname", "如何在排行榜中称呼你捏", [Cooldown(60, prompt=_lmt_notice)]
)
async def _(
    event: GroupMessageEvent,
    url: str = ArgPlainText("waka_url"),
    user_nickname: str = ArgPlainText("rank_nickname"),
):
    user_id = event.user_id

    result = await AntiEffort().add_user(int(), user_id, user_nickname, url)
    await join_global_rank.finish(result)


user_leave = AntiEffort().on_command("!我不卷了", "退出卷王统计榜")


@user_leave.handle([Cooldown(60, prompt=_lmt_notice)])
async def _user_leave(event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id

    AntiEffort().del_user(int(), user_id)
    result = AntiEffort().del_user(group_id, user_id)
    await user_leave.finish(result)


check_rank_today = AntiEffort().on_command("今日卷王", "查看今日卷王榜", aliases={"日卷王"})


@check_rank_today.handle([Cooldown(15, prompt=_lmt_notice)])
async def _check_rank_today(event: GroupMessageEvent):
    await check_rank_today.send("别急！正在统计！")

    group_id = event.group_id
    user_id = event.user_id
    raw_data = AntiEffort().get_data(group_id)
    if not raw_data:
        await check_rank_today.finish("贵群还没有人加入卷王统计榜！")

    result = AntiEffort().gen_rank(raw_data, user_id, "today")
    await check_rank_today.finish(result)


check_rank_recent_week = AntiEffort().on_command("周卷王", "查看近一周卷王榜")


@check_rank_recent_week.handle([Cooldown(15, prompt=_lmt_notice)])
async def _check_rank_recent_week(event: GroupMessageEvent):
    await check_rank_recent_week.send("别急！正在统计！")

    group_id = event.group_id
    user_id = event.user_id
    raw_data = AntiEffort().get_data(group_id)
    if not raw_data:
        await check_rank_recent_week.finish("贵群还没有人加入卷王统计榜！")

    result = AntiEffort().gen_rank(raw_data, user_id, "recent_week")
    await check_rank_recent_week.finish(result)


check_rank_global_today = AntiEffort().on_command("公共卷王", "查看今日公共卷王榜")


@check_rank_global_today.handle([Cooldown(15, prompt=_lmt_notice)])
async def _check_rank_global_today(event: MessageEvent):
    await check_rank_global_today.send("别急！正在统计！")

    user_id = event.user_id
    raw_data = AntiEffort().get_data(int())
    if not raw_data:
        await check_rank_global_today.finish("还没有人加入公共卷王统计榜！")

    result = AntiEffort().gen_rank(raw_data, user_id, "global_today")
    await check_rank_global_today.finish(result)


check_rank_global_recent_week = AntiEffort().on_command("公共周卷王", "查看近一周公共卷王榜")


@check_rank_global_recent_week.handle([Cooldown(15, prompt=_lmt_notice)])
async def _check_rank_global_recent_week(event: MessageEvent):
    await check_rank_global_recent_week.send("别急！正在统计！")

    user_id = event.user_id
    raw_data = AntiEffort().get_data(int())
    if not raw_data:
        await check_rank_global_recent_week.finish("还没有人加入公共卷王统计榜！")

    result = AntiEffort().gen_rank(raw_data, user_id, "global_recent_week")
    await check_rank_global_recent_week.finish(result)


update_data = AntiEffort().cmd_as_group("update", "更新卷王统计榜数据", permission=SUPERUSER)


@update_data.handle()
async def _update_data(event: MessageEvent):
    await AntiEffort().update_data()
    await update_data.finish("更新完成~！")


@scheduler.scheduled_job("interval", name="卷王数据更新", minutes=15, misfire_grace_time=15)  # type: ignore
async def _():
    await AntiEffort().update_data()


@scheduler.scheduled_job("cron", name="卷王数据存储", hour=0, misfire_grace_time=30)  # type: ignore
async def _():
    await AntiEffort().update_data()
    AntiEffort().store_user_data_recent()


@scheduler.scheduled_job("cron", name="对昨日卷王进行颁奖", hour=8, misfire_grace_time=30)  # type: ignore
async def _():
    files = os.listdir(PLUGIN_DIR)
    if not files:
        return

    eb_g = list()
    for f in files:
        raw_data = f.split(".")
        if raw_data[-1] != "json":
            continue

        patt = r"([0-9].*?)-ld"
        match = re.findall(patt, raw_data[0])
        if not match:
            continue

        eb_g.append(match[0])

    if not eb_g:
        return

    bot = get_bot()
    for g in eb_g:
        if not int(g):
            continue

        file_path = PLUGIN_DIR / f"{g}-ld.json"
        raw_data = json.loads(file_path.read_bytes())
        data = raw_data["data"]
        data = sorted(data, key=lambda x: x["recent_count"], reverse=True)
        winner = data[0]
        winner_id = int(winner["user_id"])
        winner_nickname = winner["user_nickname"]
        coding_time = float(winner["recent_count"])

        img = await AntiEffort().gen_img(winner_id, winner_nickname, coding_time)
        result = MessageSegment.image(img)

        try:
            await bot.send_group_msg(group_id=g, message="昨日卷王已经产生！")
            await bot.send_group_msg(group_id=g, message=Message(result))
        except Exception:
            continue
