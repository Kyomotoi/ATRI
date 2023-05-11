import pytest
from nonebug import App

from nonebot.adapters.onebot.v11 import Bot, Message

from .utils import group_message_event


@pytest.mark.asyncio
async def test_saucenao(app: App):
    from ATRI.plugins.saucenao import saucenao

    async with app.test_matcher(saucenao) as ctx:
        bot = ctx.create_bot(base=Bot)
        event = group_message_event(message=Message("以图搜图"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "图呢？", True)

        event = group_message_event(message=Message("test"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "请发送图片而不是其他东西！！", True)
        ctx.should_rejected()
