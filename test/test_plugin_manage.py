import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_block_user(app: App):
    from ATRI.plugins.manage import block_user

    Message = make_fake_message()

    async with app.test_matcher(block_user) as ctx:
        bot = ctx.create_bot()

        msg = Message("封禁用户")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "哪位？GKD！", True)

        msg = Message("114514")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "用户 114514 危！", True)


@pytest.mark.asyncio
async def test_unblock_user(app: App):
    from ATRI.plugins.manage import unblock_user

    Message = make_fake_message()

    async with app.test_matcher(unblock_user) as ctx:
        bot = ctx.create_bot()

        msg = Message("解封用户")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "哪位？GKD！", True)

        msg = Message("114514")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "好欸！ 114514 重获新生！", True)


@pytest.mark.asyncio
async def test_block_group(app: App):
    from ATRI.plugins.manage import block_group

    Message = make_fake_message()

    async with app.test_matcher(block_group) as ctx:
        bot = ctx.create_bot()

        msg = Message("封禁群")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "哪位？GKD！", True)

        msg = Message("114514")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "群 114514 危！", True)


@pytest.mark.asyncio
async def test_unblock_group(app: App):
    from ATRI.plugins.manage import unblock_group

    Message = make_fake_message()

    async with app.test_matcher(unblock_group) as ctx:
        bot = ctx.create_bot()

        msg = Message("解封群")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "哪个群？GKD！", True)

        msg = Message("114514")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "好欸！ 114514 重获新生！", True)


@pytest.mark.asyncio
async def test_global_block_service(app: App):
    from ATRI.plugins.manage import global_block_service

    Message = make_fake_message()

    async with app.test_matcher(global_block_service) as ctx:
        bot = ctx.create_bot()

        msg = Message("全局封禁")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "阿...是哪个服务呢", True)

        msg = Message("状态")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "服务 状态 已被禁用", True)


@pytest.mark.asyncio
async def test_global_unblock_service(app: App):
    from ATRI.plugins.manage import global_unblock_service

    Message = make_fake_message()

    async with app.test_matcher(global_unblock_service) as ctx:
        bot = ctx.create_bot()

        msg = Message("全局启用")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "阿...是哪个服务呢", True)

        msg = Message("状态")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "服务 状态 已启用", True)


@pytest.mark.asyncio
async def test_user_block_service(app: App):
    from ATRI.plugins.manage import user_block_service

    Message = make_fake_message()

    async with app.test_matcher(user_block_service) as ctx:
        bot = ctx.create_bot()

        msg = Message("对用户114514禁用状态")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "完成～已禁止用户 114514 使用 状态", True)


@pytest.mark.asyncio
async def test_user_unblock_service(app: App):
    from ATRI.plugins.manage import user_unblock_service

    Message = make_fake_message()

    async with app.test_matcher(user_unblock_service) as ctx:
        bot = ctx.create_bot()

        msg = Message("对用户114514启用状态")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "完成～已允许用户 114514 使用 状态", True)


@pytest.mark.asyncio
async def test_group_block_service(app: App):
    from ATRI.plugins.manage import group_block_service

    Message = make_fake_message()

    async with app.test_matcher(group_block_service) as ctx:
        bot = ctx.create_bot()

        msg = Message("禁用")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "阿...是哪个服务呢", True)

        msg = Message("状态")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "完成！～已禁止本群使用服务：状态", True)


@pytest.mark.asyncio
async def test_group_unblock_service(app: App):
    from ATRI.plugins.manage import group_unblock_service

    Message = make_fake_message()

    async with app.test_matcher(group_unblock_service) as ctx:
        bot = ctx.create_bot()

        msg = Message("启用")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "阿...是哪个服务呢", True)

        msg = Message("状态")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "完成！～已允许本群使用服务：状态", True)


@pytest.mark.asyncio
async def test_get_friend_add_list(app: App):
    from ATRI.plugins.manage import get_friend_add_list

    Message = make_fake_message()

    async with app.test_matcher(get_friend_add_list) as ctx:
        bot = ctx.create_bot()

        msg = Message("获取好友申请")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            申请人ID | 申请信息 | 申请码
            Tip: 使用 同意/拒绝好友 [申请码] 以决定
            """,
            True,
        )


# @pytest.mark.asyncio
# async def test_approve_friend_add(app: App):
#     from ATRI.plugins.manage import approve_friend_add

#     Message = make_fake_message()

#     async with app.test_matcher(approve_friend_add) as ctx:
#         bot = ctx.create_bot()

#         msg = Message("同意好友")
#         event = make_fake_event(_message=msg)()

#         ctx.receive_event(bot, event)
#         ctx.should_call_send(event, "申请码GKD!", True)

#         msg = Message()


@pytest.mark.asyncio
async def test_get_group_invite_list(app: App):
    from ATRI.plugins.manage import get_group_invite_list

    Message = make_fake_message()

    async with app.test_matcher(get_group_invite_list) as ctx:
        bot = ctx.create_bot()

        msg = Message("获取邀请列表")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            申请人ID | 申请信息 | 申请码
            Tip: 使用 同意/拒绝邀请 [申请码] 以决定
            """,
            True,
        )


@pytest.mark.asyncio
async def test_track_error(app: App):
    from ATRI.plugins.manage import track_error

    Message = make_fake_message()

    async with app.test_matcher(track_error) as ctx:
        bot = ctx.create_bot()

        msg = Message("/track")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "请检查ID是否正确...", True)
