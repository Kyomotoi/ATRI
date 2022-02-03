import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_get_laugh(app: App):
    from ATRI.plugins.funny import get_laugh

    Message = make_fake_message()

    async with app.test_matcher(get_laugh) as ctx:
        bot = ctx.create_bot()

        msg = Message("来句笑话")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "哈 哈 哈", True)


@pytest.mark.asyncio
async def test_me_re_you(app: App):
    from ATRI.plugins.funny import me_re_you

    Message = make_fake_message()

    async with app.test_matcher(me_re_you) as ctx:
        bot = ctx.create_bot()

        msg = Message("超市我")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "超市你", True)


@pytest.mark.asyncio
async def test_fake_msg(app: App):
    from ATRI.plugins.funny import fake_msg

    Message = make_fake_message()

    async with app.test_matcher(fake_msg) as ctx:
        bot = ctx.create_bot()

        msg = Message("/fakemsg")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "内容呢？格式：qq-name-content\n可构造多条，以上仅为一条，使用空格隔开", True)

        msg = Message("114514")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "内容格式错误，请检查（", True)

    async with app.test_matcher(fake_msg) as ctx:
        bot = ctx.create_bot()

        msg = Message("/fakemsg")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "内容呢？格式：qq-name-content\n可构造多条，以上仅为一条，使用空格隔开", True)

        msg = Message("114514-0w0-testing")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            "[{'type': 'node', 'data': {'name': '0w0', 'uin': '114514', 'content': 'testing'}}]",
            True,
        )

    async with app.test_matcher(fake_msg) as ctx:
        bot = ctx.create_bot()

        msg = Message("/fakemsg")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "内容呢？格式：qq-name-content\n可构造多条，以上仅为一条，使用空格隔开", True)

        msg = Message("114514-0w0-testing")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "构造失败惹...可能是被制裁了（", True)

    async with app.test_matcher(fake_msg) as ctx:
        bot = ctx.create_bot()

        msg = Message("/fakemsg")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "慢...慢一..点❤", True)


@pytest.mark.asyncio
async def test_eat_what(app: App):
    from ATRI.plugins.funny import eat_what

    Message = make_fake_message()

    async with app.test_matcher(eat_what) as ctx:
        bot = ctx.create_bot()

        msg = Message("今天吃什么")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "欧尼酱的智商低下想不到今天要吃甚么，所以由我来选择，我给的答案是(串烧)。选我正解!!", True)
