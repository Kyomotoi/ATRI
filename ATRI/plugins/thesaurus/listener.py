import re
from random import choice, shuffle

from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger

from ATRI.log import log
from ATRI.service import Service
from ATRI.utils.apscheduler import scheduler

from .data_source import ThesaurusManager, ThesaurusListener, ThesaurusStoragor


thes_listener = Service("词库监听").document("词库监听器")


class ThesaurusLinstenerIsEnabledChecker(BaseTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        conf = thes_listener.load_service("词库管理")
        if conf.get("enabled"):
            return now


async def _thesaurus_vote_listener():
    tm = ThesaurusManager()
    try:
        all_items = await tm.get_all_items(False)
    except Exception:
        return

    for i in all_items:
        data: ThesaurusStoragor = i
        item_vote_list = data.vote_list
        if len(item_vote_list) >= 10:
            t = data.m_type

            if t == 0:
                m_type = "全匹配"
            elif t == 1:
                m_type = "模糊匹配"
            else:
                m_type = "正则"

            result = await tm.add_item(
                data._id,
                True,
                data.matcher,
                list(data.result),
                data.need_at,
                m_type,
                data.group_id,
                data.operator,
                data.operator_id,
                1,
                list(data.vote_list),
            )
            log.debug(result)

            bot = get_bot()
            await bot.send_group_msg(group_id=data.group_id, message=result)


def init_listener():
    scheduler.add_job(
        _thesaurus_vote_listener,
        AndTrigger([IntervalTrigger(seconds=10), ThesaurusLinstenerIsEnabledChecker()]),
        max_instances=3,  # type: ignore
        misfire_grace_time=20,  # type: ignore
    )


async def process_message(event: MessageEvent, query_group_id: int = int()):
    tl = ThesaurusListener()
    msg = event.get_message().extract_plain_text()

    query_result = await tl.get_item_list(query_group_id)
    if not query_result:
        return

    shuffle(query_result)

    for i in query_result:
        item_info: ThesaurusStoragor = i
        if not item_info.result:
            continue

        match_type = item_info.m_type
        matcher = item_info.matcher
        if item_info.need_at and not event.is_tome():
            return
        if match_type == 1 and matcher in msg:
            await main_listener.finish(Message(choice(item_info.result)))
        elif match_type == 2 and re.findall(matcher, msg):
            await main_listener.finish(Message(choice(item_info.result)))
        elif matcher == msg:
            await main_listener.finish(Message(choice(item_info.result)))


main_listener = thes_listener.on_message(
    "词库监听器", "监听所有消息判断是否满足触发词条条件", priority=4, block=False
)


@main_listener.handle([Cooldown(3)])
async def _(event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        await process_message(event, group_id)

    await process_message(event)
