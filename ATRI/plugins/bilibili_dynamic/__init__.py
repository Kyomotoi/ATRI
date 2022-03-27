import re
from tabulate import tabulate
from datetime import datetime, timedelta

import pytz
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger

from nonebot.params import State
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, Message
from nonebot.typing import T_State
from nonebot import get_bot

from ATRI.utils.apscheduler import scheduler
from ATRI.utils import timestamp2datetime
from ATRI.log import logger

from .data_source import BilibiliDynamicSubscriptor


bilibili_dynamic = BilibiliDynamicSubscriptor().on_command(
    "/bilibili_dynamic", "b站动态订阅助手", aliases={"/bd", "b站动态"}
)

__help__ = """好哦！是b站动态订阅诶～
目前支持的功能如下...请键入对应关键词：
1.添加订阅
2.取消订阅
3.订阅列表
-----------------------------------
用法示例1：/bd 添加订阅
用法示例2：/bd 取消订阅 401742377（数字uid）
用法示例3：/bd 订阅列表"""


def help() -> str:
    return __help__


@bilibili_dynamic.handle()
async def _menu(event: GroupMessageEvent, state: T_State = State()):
    args = str(event.get_plaintext()).strip().lower().split()[1:]
    if not args:
        await bilibili_dynamic.finish(help())
    elif args and len(args) == 1:
        state["sub_command"] = args[0]
    elif args and len(args) == 2:
        state["sub_command"] = args[0]
        state["uid"] = args[1]
    else:
        await bilibili_dynamic.finish("参数错误QAQ 请检查您的输入～")


@bilibili_dynamic.got("sub_command", prompt="您要执行操作是?\n【添加订阅/取消订阅/订阅列表】")
async def handle_subcommand(event: GroupMessageEvent, state: T_State = State()):
    if state["sub_command"] not in ["添加订阅", "取消订阅", "订阅列表"]:
        await bilibili_dynamic.finish("没有这个命令哦, 请在【添加订阅/取消订阅/订阅列表】中选择并重新发送")

    if state["sub_command"] == "订阅列表":
        subscriptor = BilibiliDynamicSubscriptor()
        r = await subscriptor.get_subscriptions(query_map={"groupid": event.group_id})
        subs = []
        for s in r:
            tm = s.last_update.replace(tzinfo=pytz.timezone("Asia/Shanghai"))
            subs.append([s.nickname, s.uid, tm + timedelta(hours=8)])
        output = "本群订阅的UP列表如下～\n" + tabulate(
            subs, headers=["up名称", "UID", "上次更新时间"], tablefmt="plain", showindex=True
        )
        await bilibili_dynamic.finish(output)


@bilibili_dynamic.got("uid", prompt="请输入b站UID（输入-1取消）:")
async def handle_uid(event: GroupMessageEvent, state: T_State = State()):
    sub_command = state["sub_command"]
    if isinstance(state["uid"], list):
        uid = str(state["uid"][0])
    else:
        uid = state["uid"]

    if uid == "-1":
        await bilibili_dynamic.finish("已经成功退出订阅~")
    if not re.match(r"^\d+$", uid):
        await bilibili_dynamic.reject("这似乎不是UID呢, 请重新输入:")
    uid = int(uid)
    subscriptor = BilibiliDynamicSubscriptor()
    up_name = await subscriptor.get_upname_by_uid(uid)
    if up_name == "":
        await bilibili_dynamic.finish(f"无法获取uid={uid}的up信息...订阅失败了".format(uid=uid))
    else:
        await bilibili_dynamic.send(
            f"uid为{uid}的UP主是【{up_name}】\n{sub_command}操作中...".format(
                uid=uid, up_name=up_name, sub_command=sub_command
            )
        )
    query_result = await subscriptor.get_subscriptions(
        query_map={"uid": uid, "groupid": event.group_id}
    )
    success = True
    if sub_command == "添加订阅":
        if len(query_result) > 0:
            await bilibili_dynamic.finish(
                f"订阅失败，因为uid={uid}的UP主【{up_name}】已在本群订阅列表中".format(
                    uid=uid, up_name=up_name
                )
            )
        success = await subscriptor.add_subscription(uid, event.group_id)
        success = success and (
            await subscriptor.update_subscription_by_uid(
                uid=uid,
                update_map={"nickname": up_name, "last_update": datetime.utcnow()},
            )
        )
    elif sub_command == "取消订阅":
        if len(query_result) == 0:
            await bilibili_dynamic.finish(
                f"取消订阅失败，因为uid={uid}的UP主【{up_name}】不在本群订阅列表中".format(
                    uid=uid, up_name=up_name
                )
            )
        success = await subscriptor.remove_subscription(uid, event.group_id)
    if success:
        await bilibili_dynamic.finish(
            f"成功{sub_command}【{up_name}】的动态!".format(
                sub_command=sub_command, up_name=up_name
            )
        )
    else:
        await bilibili_dynamic.finish("诶...因为神奇的原因失败了")


from queue import Queue

# 任务队列（taskQueue）
tq = Queue()


class BilibiliDynamicCheckEnabledTrigger(BaseTrigger):
    # 自定义trigger 保证服务开启
    # 实现abstract方法 <get_next_fire_time>
    def get_next_fire_time(self, now):
        subscriptor = BilibiliDynamicSubscriptor()
        config = subscriptor.load_service("b站动态订阅")
        if config["enabled"] == False:
            return None
        else:
            return now


# 业务逻辑
# 每10s从任务队列中拉一个uid出来，调用api进行查询
# 当任务队列为空时，从数据库读取订阅列表，并塞入任务队列tq中
@scheduler.scheduled_job(
    AndTrigger([IntervalTrigger(seconds=10), BilibiliDynamicCheckEnabledTrigger()]),
    name="b站动态检查",
    max_instances=3,  # type: ignore
    misfire_grace_time=60,  # type: ignore
)
async def _check_dynamic():
    from ATRI.database.models import Subscription

    subscriptor = BilibiliDynamicSubscriptor()
    all_dynamic = await subscriptor.get_all_subscriptions()
    if tq.empty():
        for d in all_dynamic:
            tq.put(d)
    else:
        d: Subscription = tq.get()
        logger.info("准备查询UP【{up}】的动态 队列剩余{size}".format(up=d.nickname, size=tq.qsize()))
        ts = int(d.last_update.timestamp())
        info: dict = await subscriptor.get_recent_dynamic_by_uid(d.uid)
        res = []
        if info:
            if info.get("cards") is not None:
                res = subscriptor.extract_dynamics_detail(info.get("cards"))

        if len(res) == 0:
            logger.warning("获取UP【{up}】的动态为空".format(up=d.nickname))
        for i in res:
            i["name"] = d.nickname
            if ts < i["timestamp"]:
                text, pic_url = subscriptor.generate_output(pattern=i)
                output = Message(
                    [MessageSegment.text(text), MessageSegment.image(pic_url)]
                )
                bot = get_bot()
                await bot.send_group_msg(group_id=d.groupid, message=output)
                _ = await subscriptor.update_subscription_by_uid(
                    uid=d.uid,
                    update_map={"last_update": timestamp2datetime(i["timestamp"])},
                )
                break
