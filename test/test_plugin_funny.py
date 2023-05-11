import pytest
from nonebug import App

from nonebot.adapters.onebot.v11 import Bot, Message

from .utils import group_message_event


@pytest.mark.asyncio
async def test_fake_msg(app: App):
    from ATRI.plugins.funny import fake_msg

    async with app.test_matcher(fake_msg) as ctx:
        bot = ctx.create_bot(base=Bot)

        event = group_message_event(message=Message("/fakemsg"))

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "内容呢？格式：qq-name-content\n可构造多条，以上仅为一条，使用空格隔开", True)

        event = group_message_event(message=Message("114514-0w0-testing"))

        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "send_group_forward_msg",
            {
                "group_id": 10000,
                "messages": [
                    {
                        "type": "node",
                        "data": {"name": "0w0", "uin": "114514", "content": "testing"},
                    }
                ],
            },
            True,
        )
