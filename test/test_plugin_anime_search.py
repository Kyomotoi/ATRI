import pytest
from nonebug import App

from nonebot.adapters.onebot.v11 import MessageSegment

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_saucenao(app: App):
    from ATRI.plugins.saucenao import saucenao

    Message = make_fake_message()

    async with app.test_matcher(saucenao) as ctx:
        bot = ctx.create_bot()

        msg = Message("以图搜图")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "图呢？", True)

        msg = Message(
            MessageSegment.image(
                "https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/noting/88674944_p0.png"
            )
        )
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "失败了...", False)
