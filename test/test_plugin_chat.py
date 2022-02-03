import pytest
from nonebug import App
from nonebot.adapters.onebot.v11 import MessageSegment

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_chat(app: App):
    from ATRI.plugins.chat import chat

    Message = make_fake_message()

    async with app.test_matcher(chat) as ctx:
        bot = ctx.create_bot()

        msg = Message("爱你")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "是…是嘛(脸红）呐，其实咱也……", True)


@pytest.mark.asyncio
async def test_my_name_is(app: App):
    from ATRI.plugins.chat import my_name_is

    Message = make_fake_message()

    async with app.test_matcher(my_name_is) as ctx:
        bot = ctx.create_bot()

        msg = Message("叫我")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "欧尼酱想让咱如何称呼呢！0w0", True)

        msg = Message("欧尼酱")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "好~w 那咱以后就称呼你为欧尼酱！", True)


@pytest.mark.asyncio
async def test_say(app: App):
    from ATRI.plugins.chat import say

    Message = make_fake_message()

    async with app.test_matcher(say) as ctx:
        bot = ctx.create_bot()

        msg = Message("说")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "想要咱复读啥呢...", True)

        msg = Message("nya~")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "nya~", True)

    async with app.test_matcher(say) as ctx:
        bot = ctx.create_bot()

        msg = Message("说")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "想要咱复读啥呢...", True)

        msg = Message(
            MessageSegment.image(
                "https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/noting/88674944_p0.png"
            )
        )
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "不要...", True)
