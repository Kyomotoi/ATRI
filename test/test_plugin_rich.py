import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_bili_rich(app: App):
    from ATRI.plugins.rich import bili_rich

    Message = make_fake_message()

    async with app.test_matcher(bili_rich) as ctx:
        bot = ctx.create_bot()

        msg = Message("BV1Ff4y1C7YR")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            BV1Ff4y1C7YR INFO:
            Title: 【8K30fps】这可能是画质最高的Rick Roll (doge)
            Link: https://b23.tv/BV1Ff4y1C7YR
            """,
            True,
        )
