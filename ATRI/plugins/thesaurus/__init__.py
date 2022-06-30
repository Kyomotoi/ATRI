import pytz
from tabulate import tabulate

from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import ArgPlainText, CommandArg
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, GroupMessageEvent

from ATRI.utils import gen_random_str, MessageChecker

from .data_source import ThesaurusManager


add_item = ThesaurusManager().cmd_as_group("add", "添加本群词条，需审核或投票")


@add_item.handle()
async def _get_normal_item(matcher: Matcher, args: Message = CommandArg()):
    raw_msg = args.extract_plain_text()
    msg_data = raw_msg.split(" ")
    data = dict(enumerate(msg_data))
    if data.get(0):
        matcher.set_arg("ts_normal_item_q", Message(msg_data[0]))
    if data.get(1):
        matcher.set_arg("ts_normal_item_a", Message(msg_data[1]))
    if data.get(2):
        matcher.set_arg("ts_normal_item_is_need_at", Message(msg_data[2]))
    if data.get(3):
        matcher.set_arg("ts_normal_item_t", Message(msg_data[3]))


@add_item.got("ts_normal_item_q", "有人问:")
@add_item.got("ts_normal_item_a", "我答: \n(支持多个回复，用','[小写]隔开)")
@add_item.got("ts_normal_item_is_need_at", "是否需要at: (y/n)")
async def _deal_noraml_is_need_at(
    need_at: str = ArgPlainText("ts_normal_item_is_need_at"),
):
    agree_list = ["y", "Y", "是", "同意", "赞成"]
    disagree_list = ["n", "N", "否", "不", "不同意", "不赞成"]
    if need_at not in agree_list and need_at not in disagree_list:
        await add_item.reject("你的观点似乎并不相关呢...请重新输入: (y/n)")


@add_item.got("ts_normal_item_t", "问答匹配模式: \n(全匹配、模糊匹配、正则)")
async def _add_normal_item(
    bot: Bot,
    event: GroupMessageEvent,
    item_q: str = ArgPlainText("ts_normal_item_q"),
    item_a: str = ArgPlainText("ts_normal_item_a"),
    _need_at: str = ArgPlainText("ts_normal_item_is_need_at"),
    item_t: str = ArgPlainText("ts_normal_item_t"),
):
    type_list = ["全匹配", "模糊匹配", "正则"]
    if item_t not in type_list:
        await add_item.finish("该类型不支持 (全匹配、模糊匹配、正则)\n请重新提交.")

    q_checker = MessageChecker(item_q).check_cq_code
    a_checker = MessageChecker(item_a).check_cq_code
    if not q_checker or not a_checker:
        await add_item.finish("请不要尝试注入！")

    agree_list = ["y", "Y", "是", "同意", "赞成"]
    need_at = 1 if _need_at in agree_list else 0

    group_id = event.group_id
    operator_id = event.user_id
    operator_info = await bot.get_group_member_info(
        group_id=group_id, user_id=operator_id
    )
    operator = operator_info.get("card", "unknown")
    item_id = gen_random_str(6)
    ans = item_a.split(",")
    ts = ThesaurusManager()

    result = await ts.add_item(
        item_id,
        False,
        item_q,
        ans,
        need_at,
        item_t,
        group_id,
        operator,
        operator_id,
        1,
        list(),
    )
    await add_item.finish(result)


add_item_as_group_admin = ThesaurusManager().cmd_as_group(
    "add.g", "添加本群词条，仅限管理，无需审核", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN
)


@add_item_as_group_admin.handle()
async def _get_group_item(matcher: Matcher, args: Message = CommandArg()):
    raw_msg = args.extract_plain_text()
    msg_data = raw_msg.split(" ")
    data = dict(enumerate(msg_data))
    if data.get(0):
        matcher.set_arg("ts_group_item_q", Message(msg_data[0]))
    if data.get(1):
        matcher.set_arg("ts_group_item_a", Message(msg_data[1]))
    if data.get(2):
        matcher.set_arg("ts_group_item_is_need_at", Message(msg_data[2]))
    if data.get(3):
        matcher.set_arg("ts_group_item_t", Message(msg_data[3]))


@add_item_as_group_admin.got("ts_group_item_q", "有人问:")
@add_item_as_group_admin.got("ts_group_item_a", "我答: \n(支持多个回复，用','[小写]隔开)")
@add_item_as_group_admin.got("ts_group_item_is_need_at", "是否需要at: (y/n)")
async def _deal_group_is_need_at(
    need_at: str = ArgPlainText("ts_group_item_is_need_at"),
):
    agree_list = ["y", "Y", "是", "同意", "赞成"]
    disagree_list = ["n", "N", "否", "不", "不同意", "不赞成"]
    if need_at not in agree_list and need_at not in disagree_list:
        await add_item_as_group_admin.reject("你的观点似乎并不相关呢...请重新输入: (y/n)")


@add_item_as_group_admin.got("ts_group_item_t", "问答匹配模式: \n(全匹配、模糊匹配、正则)")
async def _add_group_item(
    bot: Bot,
    event: GroupMessageEvent,
    item_q: str = ArgPlainText("ts_group_item_q"),
    item_a: str = ArgPlainText("ts_group_item_a"),
    _need_at: str = ArgPlainText("ts_group_item_is_need_at"),
    item_t: str = ArgPlainText("ts_group_item_t"),
):
    type_list = ["全匹配", "模糊匹配", "正则"]
    if item_t not in type_list:
        await add_item_as_group_admin.finish("该类型不支持 (全匹配、模糊匹配、正则)\n请重新提交.")

    q_checker = MessageChecker(item_q).check_cq_code
    a_checker = MessageChecker(item_a).check_cq_code
    if not q_checker or not a_checker:
        await add_item_as_group_admin.finish("请不要尝试注入！")

    agree_list = ["y", "Y", "是", "同意", "赞成"]
    need_at = 1 if _need_at in agree_list else 0

    group_id = event.group_id
    operator_id = event.user_id
    operator_info = await bot.get_group_member_info(
        group_id=group_id, user_id=operator_id
    )
    operator = operator_info.get("card", "unknown")
    item_id = gen_random_str(6)
    ans = item_a.split(",")
    ts = ThesaurusManager()

    result = await ts.add_item(
        item_id,
        True,
        item_q,
        ans,
        need_at,
        item_t,
        group_id,
        operator,
        operator_id,
        0,
        list(),
    )
    await add_item_as_group_admin.finish(result)


add_item_for_global = ThesaurusManager().cmd_as_group(
    "add.glo", "添加全局问答", permission=SUPERUSER
)


@add_item_for_global.handle()
async def _get_global_item(matcher: Matcher, args: Message = CommandArg()):
    raw_msg = args.extract_plain_text()
    msg_data = raw_msg.split(" ")
    data = dict(enumerate(msg_data))

    if data.get(0):
        matcher.set_arg("ts_global_item_q", Message(msg_data[0]))
    if data.get(1):
        matcher.set_arg("ts_global_item_a", Message(msg_data[1]))
    if data.get(2):
        matcher.set_arg("ts_global_is_need_at", Message(msg_data[2]))
    if data.get(3):
        matcher.set_arg("ts_global_item_type", Message(msg_data[3]))


@add_item_for_global.got("ts_global_item_q", "有人问:")
@add_item_for_global.got("ts_global_item_a", "我答: \n(支持多个回复，用','[小写]隔开)")
@add_item_for_global.got("ts_global_item_is_need_at", "是否需要at: (y/n)")
async def _deal_global_is_need_at(
    event: MessageEvent, need_at: str = ArgPlainText("ts_global_item_is_need_at")
):
    agree_list = ["y", "Y", "是", "同意", "赞成"]
    disagree_list = ["n", "N", "否", "不", "不同意", "不赞成"]
    if need_at not in agree_list and need_at not in disagree_list:
        await add_item_for_global.reject("你的观点似乎并不相关呢...请重新输入: (y/n)")


@add_item_for_global.got("ts_global_item_type", "问答匹配模式: \n(全匹配、模糊匹配、正则)")
async def _add_global_item(
    event: MessageEvent,
    item_q: str = ArgPlainText("ts_global_item_q"),
    item_a: str = ArgPlainText("ts_global_item_a"),
    _need_at: str = ArgPlainText("ts_global_item_is_need_at"),
    item_t: str = ArgPlainText("ts_global_item_type"),
):
    type_list = ["全匹配", "模糊匹配", "正则"]
    if item_t not in type_list:
        await add_item_for_global.finish("该类型不支持 (全匹配、模糊匹配、正则)\n请重新提交.")

    agree_list = ["y", "Y", "是", "同意", "赞成"]
    need_at = 1 if _need_at in agree_list else 0

    operator = "SUPERUSER"
    opeartor_id = event.user_id
    item_id = gen_random_str(6)
    ans = item_a.split(",")
    tm = ThesaurusManager()

    result = await tm.add_item(
        item_id, True, item_q, ans, need_at, item_t, 0, operator, opeartor_id, 0, list()
    )
    await add_item_for_global.finish(result)


vote = ThesaurusManager().cmd_as_group("v", "对本群内审核中的词条进行投票")


@vote.handle()
async def _get_vote_info(matcher: Matcher, args: Message = CommandArg()):
    raw_msg = args.extract_plain_text()
    msg_data = raw_msg.split(" ")
    data = dict(enumerate(msg_data))
    if data.get(0):
        matcher.set_arg("ts_vote_id", Message(msg_data[0]))
    if data.get(1):
        matcher.set_arg("ts_vote_attitude", Message(msg_data[1]))


@vote.got("ts_vote_id", "要投票的词条id是:")
async def _get_item_id(
    event: GroupMessageEvent, item_id: str = ArgPlainText("ts_vote_id")
):
    tm = ThesaurusManager()
    user_id = event.user_id
    group_id = event.group_id

    query_result = await tm.get_item_list({"_id": item_id, "group_id": group_id})
    if not query_result:
        await vote.finish("未找到此id相关信息...请检查是否输入正确（")

    item_info = query_result[0]
    if user_id in item_info.vote_list:
        await vote.finish("你已经参与过啦！")

    result = f"""你即将要投票的词条信息:
    词条ID: {item_info._id}
    有人问: {item_info.matcher}
    我答: {"、".join(map(str, item_info.result))}
    提交人: {item_info.operator}@{item_info.operator_id}
    当前赞成: {"、".join(map(str, item_info.vote_list))}
    """.strip()
    await vote.send(Message(result))


@vote.got("ts_vote_attitude", "你的选择是？(y/n)")
async def _get_voter_attitude(
    event: GroupMessageEvent,
    item_id: str = ArgPlainText("ts_vote_id"),
    attitude: str = ArgPlainText("ts_vote_attitude"),
):
    agree_list = ["y", "Y", "是", "同意", "赞成"]
    disagree_list = ["n", "N", "否", "不", "不同意", "不赞成"]
    if attitude not in agree_list and attitude not in disagree_list:
        await vote.reject("你的观点似乎不相关呢...请重新输入: (y/n)")

    tm = ThesaurusManager()
    group_id = event.group_id
    user_id = event.user_id

    if attitude in agree_list:
        await tm.vote(item_id, group_id, user_id)
        await vote.finish(f"已赞成此词条～ ID: {item_id}")
    else:
        await vote.finish("好吧...")


del_item = ThesaurusManager().cmd_as_group(
    "del", "删除本群词条", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN
)


@del_item.handle()
async def _get_del_normal_item_info(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("ts_del_normal_item_id", args)


@del_item.got("ts_del_item_id", "要删除词条的id是？")
async def _deal_del_normal_item(
    event: GroupMessageEvent, item_id: str = ArgPlainText("ts_del_item_id")
):
    tm = ThesaurusManager()
    group_id = event.group_id

    result = await tm.del_item(item_id, group_id, True)
    await del_item.finish(result)


del_global_item = ThesaurusManager().cmd_as_group(
    "del.g", "删除全局词条", permission=SUPERUSER
)


@del_global_item.handle()
async def _get_del_global_item_info(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("ts_del_global_item_id", args)


@del_global_item.got("ts_del_global_item_id", "要删除词条的id是？")
async def _deal_del_global_item(
    event: GroupMessageEvent, item_id: str = ArgPlainText("ts_del_global_item_id")
):
    tm = ThesaurusManager()

    result = await tm.del_item(item_id, 0, True)
    await del_global_item.finish(result)


del_vote_item = ThesaurusManager().cmd_as_group(
    "del.v", "删除本群处于投票中的词条", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN
)


@del_vote_item.handle()
async def _get_deal_vote_item_info(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("ts_del_vote_item_id", args)


@del_vote_item.got("ts_del_vote_item_id", "要删除词条的id是？")
async def _deal_del_vote_item(
    event: GroupMessageEvent, item_id: str = ArgPlainText("ts_del_vote_item_id")
):
    tm = ThesaurusManager()
    group_id = event.group_id

    result = await tm.del_item(item_id, group_id, False)
    await del_vote_item.finish(result)


_LIST_SHOW_DATA: dict = dict()


list_item = ThesaurusManager().cmd_as_group("list", "查看本群词条")


@list_item.handle()
async def _get_normal_item_list(event: GroupMessageEvent):
    tm = ThesaurusManager()
    group_id = event.group_id

    query_result = await tm.get_item_list({"group_id": group_id}, True)
    if not query_result:
        await list_item.finish("本群还没有词条呢...")

    items = list()
    for i in query_result[:10]:
        item_matcher = i.matcher
        item_type = i.m_type
        if item_type == 0:
            m_type = "全匹配"
        elif item_type == 1:
            m_type = "模糊匹配"
        else:
            m_type = "正则"

        items.append([i._id, item_matcher, m_type])

    output = (
        "本群已添加以下词条:\n"
        + tabulate(items, headers=["ID", "匹配词", "判断方式"], tablefmt="plain")
        + "\n(一页仅展示10个)"
    )

    if len(query_result) > 10:
        await list_item.send(output)
    else:
        await list_item.finish(output)


@list_item.got("item_normal_is_next", "回复'下一页'或'n'以继续查看，任意回复以退出～")
async def _get_normal_item_more(
    event: GroupMessageEvent, is_next: str = ArgPlainText("item_normal_is_next")
):
    user_id = event.user_id
    group_id = event.group_id

    judge_list = ["下一页", "n", "next"]
    if is_next not in judge_list:
        try:
            del _LIST_SHOW_DATA[group_id][user_id]
        except Exception:
            pass
        await list_item.finish("结束查看～")

    if group_id in _LIST_SHOW_DATA:
        _LIST_SHOW_DATA[group_id][user_id] += 10
    else:
        _LIST_SHOW_DATA[group_id] = {user_id: 10}

    tm = ThesaurusManager()
    items = list()
    show_item = _LIST_SHOW_DATA[group_id][user_id]
    query_result = await tm.get_item_list({"group_id": group_id}, True)
    for i in query_result[:show_item]:
        item_matcher = i.matcher
        item_type = i.m_type
        if item_type == 0:
            m_type = "全匹配"
        elif item_type == 1:
            m_type = "模糊匹配"
        else:
            m_type = "正则"

        items.append([i._id, item_matcher, m_type])

    output = (
        tabulate(items, headers=["ID", "匹配词", "判断方式"], tablefmt="plain")
        + "\n('下一页'或'n'以继续查看，任意回复以退出)"
    )
    await list_item.reject(output)


list_global_item = ThesaurusManager().cmd_as_group("list.g", "查看全局词条")


@list_global_item.handle()
async def _get_global_item_list(event: MessageEvent):
    tm = ThesaurusManager()

    query_result = await tm.get_item_list({"group_id": 0}, True)
    if not query_result:
        await list_global_item.finish("还没有给咱添加全局词条呢...")

    items = list()
    for i in query_result[:10]:
        item_matcher = i.matcher
        item_type = i.m_type
        if item_type == 0:
            m_type = "全匹配"
        elif item_type == 1:
            m_type = "模糊匹配"
        else:
            m_type = "正则"

        items.append([i._id, item_matcher, m_type])

    output = (
        "咱已装载以下词条:\n"
        + tabulate(items, headers=["ID", "匹配词", "判断方式"], tablefmt="plain")
        + "\n(一页仅展示10个)"
    )

    if len(query_result) > 10:
        await list_global_item.send(output)
    else:
        await list_global_item.finish(output)


@list_global_item.got("item_global_is_next", "回复'下一页'或'n'以继续查看，任意回复以退出～")
async def _get_global_item_more(
    event: MessageEvent, is_next: str = ArgPlainText("item_global_is_next")
):
    user_id = event.user_id

    judge_list = ["下一页", "n", "next"]
    if is_next not in judge_list:
        try:
            del _LIST_SHOW_DATA[user_id]
        except Exception:
            pass
        await list_global_item.finish("结束查看～")

    if user_id in _LIST_SHOW_DATA:
        _LIST_SHOW_DATA[user_id] += 10
    else:
        _LIST_SHOW_DATA[user_id] = 10

    tm = ThesaurusManager()
    items = list()
    show_item = _LIST_SHOW_DATA[user_id]
    query_result = await tm.get_item_list({"group_id": 0}, True)
    for i in query_result[:show_item]:
        item_matcher = i.matcher
        item_type = i.m_type
        if item_type == 0:
            m_type = "全匹配"
        elif item_type == 1:
            m_type = "模糊匹配"
        else:
            m_type = "正则"

        items.append([i._id, item_matcher, m_type])

    output = (
        tabulate(items, headers=["ID", "匹配词", "判断方式"], tablefmt="plain")
        + "\n('下一页'或'n'以继续查看，任意回复以退出)"
    )
    await list_global_item.reject(output)


list_vote_item = ThesaurusManager().cmd_as_group("list.v", "查看本群待投票词条")


@list_vote_item.handle()
async def _get_vote_item_list(event: GroupMessageEvent):
    tm = ThesaurusManager()
    group_id = event.group_id

    query_result = await tm.get_item_list({"group_id": group_id})
    if not query_result:
        await list_vote_item.finish("本群暂未添加待审核词条...")

    items = list()
    for i in query_result[:10]:
        item_matcher = i.matcher
        item_type = i.m_type
        if item_type == 0:
            m_type = "全匹配"
        elif item_type == 1:
            m_type = "模糊匹配"
        else:
            m_type = "正则"

        items.append([i._id, item_matcher, m_type])

    output = (
        "当前待审词条概况如下:\n"
        + tabulate(items, headers=["ID", "匹配词", "判断方式"], tablefmt="plain")
        + "\n(一页仅展示10个)"
    )

    if len(query_result) > 10:
        await list_vote_item.send(output)
    else:
        await list_vote_item.finish(output)


@list_vote_item.got("item_vote_is_next", "回复'下一页'或'n'以继续查看，任意回复以退出～")
async def _get_vote_item_more(
    event: GroupMessageEvent, is_next: str = ArgPlainText("item_vote_is_next")
):
    user_id = event.user_id
    group_id = event.group_id

    judge_list = ["下一页", "n", "next"]
    if is_next not in judge_list:
        try:
            del _LIST_SHOW_DATA[group_id][user_id]
        except Exception:
            pass
        await list_vote_item.finish("结束查看～")

    if group_id in _LIST_SHOW_DATA:
        _LIST_SHOW_DATA[group_id][user_id] += 10
    else:
        _LIST_SHOW_DATA[group_id] = {user_id: 10}

    tm = ThesaurusManager()
    items = list()
    show_item = _LIST_SHOW_DATA[group_id][user_id]
    query_result = await tm.get_item_list({"group_id": group_id})
    for i in query_result[:show_item]:
        item_matcher = i.matcher
        item_type = i.m_type
        if item_type == 0:
            m_type = "全匹配"
        elif item_type == 1:
            m_type = "模糊匹配"
        else:
            m_type = "正则"

        items.append([i._id, item_matcher, m_type])

    output = (
        tabulate(items, headers=["ID", "匹配词", "判断方式"], tablefmt="plain")
        + "\n('下一页'或'n'以继续查看，任意回复以退出)"
    )
    await list_vote_item.reject(output)


audit_item = ThesaurusManager().cmd_as_group(
    "audit", "审核本群处于投票中的词条", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN
)


@audit_item.handle()
async def _get_group_item_info(matcher: Matcher, args: Message = CommandArg()):
    raw_msg = args.extract_plain_text()
    msg_data = raw_msg.split(" ")
    data = dict(enumerate(msg_data))
    if data.get(0):
        matcher.set_arg("ts_audit_vote_id", Message(msg_data[0]))
    if data.get(1):
        matcher.set_arg("ts_audit_vote_attitude", Message(msg_data[1]))


@audit_item.got("ts_audit_vote_id", "要审核的词条id是:")
async def _get_audit_item_id(
    event: GroupMessageEvent, item_id: str = ArgPlainText("ts_group_vote_id")
):
    tm = ThesaurusManager()
    group_id = event.group_id

    query_result = await tm.get_item_list({"_id": item_id, "group_id": group_id})
    if not query_result:
        await audit_item.finish("未找到此id相关信息...请检查是否输入正确（")

    item_info = query_result[0]
    result = f"""你即将要审核的词条信息:
    词条ID: {item_info._id}
    有人问: {item_info.matcher}
    我答: {"、".join(map(str, item_info.result))}
    提交人: {item_info.operator}@{item_info.operator_id}
    当前赞成: {"、".join(map(str, item_info.vote_list))}
    """.strip()
    await audit_item.send(Message(result))


@audit_item.got("ts_audit_vote_attitude", "你的选择是？(y/n)")
async def _get_audit_attitude(
    event: GroupMessageEvent,
    item_id: str = ArgPlainText("ts_audit_vote_id"),
    attitude: str = ArgPlainText("ts_audit_vote_attitude"),
):
    agree_list = ["y", "Y", "是", "同意", "赞成"]
    disagree_list = ["n", "N", "否", "不", "不同意", "不赞成"]
    if attitude not in agree_list and attitude not in disagree_list:
        await audit_item.reject("你的观点似乎不相关呢...请重新输入: (y/n)")

    tm = ThesaurusManager()
    group_id = event.group_id

    query_result = await tm.get_item_list({"_id": item_id, "group_id": group_id})
    if not query_result:
        await audit_item.finish("未找到相关内容...请检查输入...")
    item_info = query_result[0]

    if attitude in agree_list:
        await tm.add_item(
            item_id,
            True,
            item_info.matcher,
            item_info.result,
            item_info.need_at,
            item_info.m_type,
            group_id,
            item_info.operator,
            item_info.operator_id,
            0,
            list(),
        )
        await tm.del_item(item_id, group_id, False)
    else:
        await tm.del_item(item_id, group_id, False)

    await audit_item.finish("完成～！")


_ITEM_SHOW_FORMAT = """该词条信息如下:
词条ID: {_id}
有人问: {matcher}
我答: {ans}
判断方式: {m_type}
提交人: {operator}@{operator_id}
更新时间: {update_time}
是否为投票选出: {is_vote}
投票赞成: {vote_list}
"""


get_normal_item_info = ThesaurusManager().cmd_as_group("i", "查看本群的词条详情")


@get_normal_item_info.handle()
async def _info_normal_get_item_id(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("info_normal_item_id", args)


@get_normal_item_info.got("info_normal_item_id", "需要查看的词条ID:")
async def _info_normal_get_item_info(
    event: GroupMessageEvent, _id: str = ArgPlainText("info_normal_item_id")
):
    tm = ThesaurusManager()
    group_id = event.group_id

    query_result = await tm.get_item_list({"_id": _id, "group_id": group_id}, True)
    if not query_result:
        await get_normal_item_info.finish("未找到此ID相关信息...")

    item_info = query_result[0]

    item_type = item_info.m_type
    if item_type == 1:
        m_type = "模糊匹配"
    elif item_type == 2:
        m_type = "正则"
    else:
        m_type = "全匹配"

    result = _ITEM_SHOW_FORMAT.format(
        _id=_id,
        matcher=item_info.matcher,
        ans="、".join(map(str, item_info.result)),
        m_type=m_type,
        operator=item_info.operator,
        operator_id=item_info.operator_id,
        update_time=item_info.update_time.replace(
            tzinfo=pytz.timezone("Asia/Shanghai")
        ),
        is_vote="是" if item_info.is_vote else "否",
        vote_list=item_info.vote_list,
    )
    await get_normal_item_info.finish(result)


get_global_item_info = ThesaurusManager().cmd_as_group("i.g", "查看全局的词条详情")


@get_global_item_info.handle()
async def _info_global_get_item_id(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("info_global_item_id", args)


@get_global_item_info.got("info_global_item_id", "需要查看的词条ID:")
async def _info_global_get_item_info(_id: str = ArgPlainText("info_global_item_id")):
    tm = ThesaurusManager()

    query_result = await tm.get_item_list({"_id": _id, "group_id": 0}, True)
    if not query_result:
        await get_global_item_info.finish("未找到此ID相关信息...")

    item_info = query_result[0]

    item_type = item_info.m_type
    if item_type == 1:
        m_type = "模糊匹配"
    elif item_type == 2:
        m_type = "正则"
    else:
        m_type = "全匹配"

    result = _ITEM_SHOW_FORMAT.format(
        _id=_id,
        matcher=item_info.matcher,
        ans="、".join(map(str, item_info.result)),
        m_type=m_type,
        operator=item_info.operator,
        operator_id=item_info.operator_id,
        update_time=item_info.update_time.replace(
            tzinfo=pytz.timezone("Asia/Shanghai")
        ),
        is_vote="是" if item_info.is_vote else "否",
        vote_list=item_info.vote_list,
    )
    await get_global_item_info.finish(result)


get_vote_item_info = ThesaurusManager().cmd_as_group("i.v", "查看本群的待审核/投票的词条详情")


@get_vote_item_info.handle()
async def _info_vote_get_item_id(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("info_vote_item_id", args)


@get_vote_item_info.got("info_vote_item_id", "需要查看的词条ID:")
async def _info_vote_get_item_info(
    event: GroupMessageEvent, _id: str = ArgPlainText("info_vote_item_id")
):
    tm = ThesaurusManager()
    group_id = event.group_id

    query_result = await tm.get_item_list({"_id": _id, "group_id": group_id})
    if not query_result:
        await get_vote_item_info.finish("未找到此ID相关信息...")

    item_info = query_result[0]

    item_type = item_info.m_type
    if item_type == 1:
        m_type = "模糊匹配"
    elif item_type == 2:
        m_type = "正则"
    else:
        m_type = "全匹配"

    result = _ITEM_SHOW_FORMAT.format(
        _id=_id,
        matcher=item_info.matcher,
        ans="、".join(map(str, item_info.result)),
        m_type=m_type,
        operator=item_info.operator,
        operator_id=item_info.operator_id,
        update_time=item_info.update_time.replace(
            tzinfo=pytz.timezone("Asia/Shanghai")
        ),
        is_vote="是" if item_info.is_vote else "否",
        vote_list=item_info.vote_list,
    )
    await get_vote_item_info.finish(result)


from ATRI import driver

from .listener import init_listener


driver().on_startup(init_listener)
