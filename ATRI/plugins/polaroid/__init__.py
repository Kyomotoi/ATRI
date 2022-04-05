from random import choice

from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.rule import to_bot
from .data_source import Polaroid, TEMP_PATH


_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


polaroid = Polaroid().on_command("拍立得", "获取一张以自己头像的拍立得图片！需at", rule=to_bot())


@polaroid.handle([Cooldown(15, prompt=_flmt_notice)])
async def _(event: MessageEvent):
    user_id = event.get_user_id()

    temp_p = TEMP_PATH / f"{user_id}.png"
    if not temp_p.is_file():
        pol = await Polaroid().generate(user_id)
        result = MessageSegment.image(pol)
    else:
        result = MessageSegment.image(temp_p)

    await polaroid.finish(Message(result))
