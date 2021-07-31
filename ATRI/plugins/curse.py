from random import choice

from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import is_in_service, to_bot
from ATRI.service import Service
from ATRI.utils import request
from ATRI.utils.limit import FreqLimiter


URL = "https://zuanbot.com/api.php?level=min&lang=zh_cn"

_curse_flmt = FreqLimiter(3)
_curse_flmt_notice = choice(["我看你是找🔨是吧", "给我适可而止阿！？", "扎布多得了😅", "z？是m吗？我凑那也太恐怖了", "?"])


__doc__ = """
口臭！你急了你急了！
"""


class Curse(Service):
    def __init__(self):
        Service.__init__(self, "口臭", __doc__, rule=is_in_service("口臭"))

    @staticmethod
    async def now() -> str:
        res = await request.get(URL)
        result = await res.text  # type: ignore
        return result


normal_curse = Curse().on_command(
    "口臭一下", "主命令，骂你一下", aliases={"骂我", "口臭"}, rule=to_bot()
)


@normal_curse.handle()
async def _deal_n_curse(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _curse_flmt.check(user_id):
        await normal_curse.finish(_curse_flmt_notice)

    result = await Curse().now()
    _curse_flmt.start_cd(user_id)
    await normal_curse.finish(result)


super_curse = Curse().on_regex(r"[来求有](.*?)骂我吗?", "有求必应")


@super_curse.handle()
async def _deal_s_curse(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _curse_flmt.check(user_id):
        await normal_curse.finish(_curse_flmt_notice)

    result = await Curse().now()
    _curse_flmt.start_cd(user_id)
    await normal_curse.finish(result)
