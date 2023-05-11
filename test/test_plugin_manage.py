from typing import Type, Union

import pytest
from nonebug import App

from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

from ATRI.permission import toggle_master
from .utils import group_message_event


async def __test_wrapper(
    app: App,
    test_matcher: Type[Matcher],
    test_command: str,
    test_arg: Union[str, MessageSegment],
    test_reply: str,
):
    async with app.test_matcher(test_matcher) as ctx:
        bot = ctx.create_bot(base=Bot)
        event = group_message_event(message=Message(test_command))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "要操作的目标是？", True)

        event = group_message_event(message=Message(test_arg))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, test_reply, True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_manage(app: App):
    await toggle_master("1145141919")

    from ATRI.plugins.manage import block_user

    await __test_wrapper(app, block_user, "封禁用户", "114514", "用户 114514 危！")

    from ATRI.plugins.manage import unblock_user

    await __test_wrapper(app, unblock_user, "解封用户", "114514", "用户 114514 已解封")

    from ATRI.plugins.manage import block_group

    await __test_wrapper(app, block_group, "封禁群", "114514", "群 114514 危！")

    from ATRI.plugins.manage import unblock_group

    await __test_wrapper(app, unblock_group, "解封群", "114514", "群 114514 已解封")

    from ATRI.plugins.manage import toggle_global_service

    await __test_wrapper(app, toggle_global_service, "全局控制", "涩图", "服务 涩图 已全局禁用")
    await __test_wrapper(app, toggle_global_service, "全局控制", "涩图", "服务 涩图 已全局启用")

    from ATRI.plugins.manage import toggle_group_service

    await __test_wrapper(app, toggle_group_service, "控制", "涩图", "服务 涩图 已针对本群禁用")
    await __test_wrapper(app, toggle_group_service, "控制", "涩图", "服务 涩图 已针对本群启用")

    from ATRI.plugins.manage import track_error

    await __test_wrapper(
        app, track_error, "追踪", "abcdefg", "操作 abcdefg 失败...原因：\n未找到对应ID的信息"
    )

    from ATRI.plugins.manage import toggle_user_service

    async with app.test_matcher(toggle_user_service) as ctx:
        bot = ctx.create_bot(base=Bot)
        event = group_message_event(message=Message("对用户114514禁用涩图"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "已禁止用户 114514 使用 涩图", True)
        ctx.should_finished()

    async with app.test_matcher(toggle_user_service) as ctx:
        bot = ctx.create_bot(base=Bot)
        event = group_message_event(message=Message("对用户114514启用涩图"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "已允许用户 114514 使用 涩图", True)
        ctx.should_finished()

    await toggle_master("1145141919")
