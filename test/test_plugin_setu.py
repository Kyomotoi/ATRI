import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_random_setu(app: App):
    from ATRI.plugins.setu import random_setu

    Message = make_fake_message()

    async with app.test_matcher(random_setu) as ctx:
        bot = ctx.create_bot()

        msg = Message("来张涩图")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "hso（发不出", False)
