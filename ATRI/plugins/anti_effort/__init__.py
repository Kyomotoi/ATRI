from tabulate import tabulate
from datetime import datetime

from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent

from .data_source import AntiEffort


_GET_URL_MSG = """请键入wakatime share embed URL:
获取方法:
  - 前往 wakatime.com/share/embed
  - Format 选择 JSON
  - Chart Type 选择 Coding Activity
  - Date Range 选择 Last 7 Days
  - 所需url就在下一栏 HTML 中的 url
""".strip()


add_user = AntiEffort().on_command("!我也要卷", "加入卷王统计榜")
add_user_cmd = AntiEffort().cmd_as_group("join", "加入卷王统计榜")


@add_user.got("waka_url", _GET_URL_MSG)
@add_user_cmd.got("waka_url", _GET_URL_MSG)
@add_user.got("rank_nickname", "如何在排行榜中称呼你捏")
@add_user_cmd.got("rank_nickname", "如何在排行榜中称呼你捏")
async def _deal_add_user(
    event: GroupMessageEvent,
    _url: str = ArgPlainText("waka_url"),
    user_nickname: str = ArgPlainText("rank_nickname"),
):
    group_id = event.group_id
    user_id = event.user_id

    result = AntiEffort().add_user(group_id, user_id, user_nickname, _url)
    await add_user.finish(result)


user_leave = AntiEffort().on_command("!我不卷了", "退出卷王统计榜")
user_leave_cmd = AntiEffort().cmd_as_group("leave", "退出卷王统计榜")


@user_leave.handle()
@user_leave_cmd.handle()
async def _user_leave(event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id

    result = AntiEffort().del_user(group_id, user_id)
    await user_leave.finish(result)


check_rank_today = AntiEffort().on_command("今日卷王", "查看今日卷王榜")
check_rank_today_cmd = AntiEffort().cmd_as_group("rank.today", "查看今日卷王榜")


@check_rank_today.handle()
@check_rank_today_cmd.handle()
async def _check_rank_today(event: GroupMessageEvent):
    await check_rank_today.send("别急！正在统计！")

    group_id = event.group_id
    u = await AntiEffort().update_data()
    if u == 114514:
        await check_rank_today.finish("贵群还没有人加入卷王统计榜！")

    data = AntiEffort().get_data(group_id)
    if not data:
        await check_rank_today.finish("贵群还没有人加入卷王统计榜！")

    data = sorted(data, key=lambda x: x["recent_count"], reverse=True)
    table = [
        [
            f"{i + 1}",
            f"{x['user_nickname']}",
            f"{round(x['recent_count'], 2)}",
        ]
        for i, x in enumerate(data)
    ]
    table.insert(0, ["Rank", "Member", "Today"])
    result = tabulate(table, tablefmt="plain")
    now_time = datetime.now().strftime("%Y/%m/%d")
    repo = f"《今日卷王》 单位: 小时\nRank Date: {now_time}\n{result}"
    await check_rank_today.finish(repo)


check_rank_recent_week = AntiEffort().on_command("周卷王", "查看近一周卷王榜")
check_rank_recent_week_cmd = AntiEffort().cmd_as_group("rank.week", "查看近一周卷王榜")


@check_rank_recent_week.handle()
@check_rank_recent_week_cmd.handle()
async def _check_rank_recent_week(event: GroupMessageEvent):
    await check_rank_recent_week.send("别急！正在统计！")

    group_id = event.group_id
    u = await AntiEffort().update_data()
    if u == 114514:
        await check_rank_recent_week.finish("贵群还没有人加入卷王统计榜！")

    data = AntiEffort().get_data(group_id)
    if not data:
        await check_rank_recent_week.finish("贵群还没有人加入卷王统计榜！")

    data = sorted(data, key=lambda x: x["last_7_days_count"], reverse=True)
    table = [
        [
            f"{i + 1}",
            f"{x['user_nickname']}",
            f"{round(x['last_7_days_count'], 2)}",
        ]
        for i, x in enumerate(data)
    ]
    table.insert(0, ["Rank", "Member", "Last 7 Days"])
    result = tabulate(table, tablefmt="plain")
    now_time = datetime.now().strftime("%Y/%m/%d")
    repo = f"《近一周卷王》 单位: 小时\nRank Date: {now_time}\n{result}"
    await check_rank_recent_week.finish(repo)
