import asyncio
from random import choice
from pydantic import BaseModel

from nonebot.rule import Rule
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.helpers import Cooldown

from .data_source import Wife


_is_tietie = True


tietie_superuser = Wife().on_message(
    "贴贴",
    "只与维护者贴贴w，‘不可以贴’以拒绝贴贴~，‘来贴贴’以接受贴贴~",
    rule=Rule(),
    permission=SUPERUSER,
    block=False,
)


@tietie_superuser.handle([Cooldown(600)])
async def _tietie_superuser(event: MessageEvent):
    if not _is_tietie:
        await tietie_superuser.finish()

    user_id = event.get_user_id()
    result = Wife().to_superuser(user_id)
    await tietie_superuser.finish(Message(result))


no_tietie = Wife().on_command("不可以贴", docs="拒绝贴贴", rule=Rule(), permission=SUPERUSER)


@no_tietie.handle()
async def _no_tietie():
    global _is_tietie
    _is_tietie = False
    await no_tietie.finish("好吧...")


yes_tietie = Wife().on_command("来贴贴", docs="继续贴贴", rule=Rule(), permission=SUPERUSER)


@yes_tietie.handle()
async def _yes_tietie():
    global _is_tietie
    _is_tietie = True
    await yes_tietie.finish("好欸！")


class MarryInfo(BaseModel):
    name: str
    sex: str
    wife: str


get_wife = Wife().on_command("抽老婆", "随机选择一位幸运裙友成为老婆！")


@get_wife.handle([Cooldown(10)])
async def _get_wife(bot: Bot, event: GroupMessageEvent):
    user_id = event.get_user_id()

    data = Wife().load_marry_list()
    if user_id in data:
        await get_wife.finish("你已经有对象了哦~（")

    group_id = event.group_id
    req_user_info: dict = await bot.get_group_member_info(
        group_id=group_id, user_id=int(user_id)
    )

    req_user_card = req_user_info["card"]
    if not req_user_card:
        req_user_card = req_user_info["nickname"]

    req_user_sex = req_user_info["sex"]
    is_nick = "老公" if req_user_sex == "male" else "老婆"

    repo_0 = f"现在咱将随机抽取一位幸运裙友\n成为{req_user_card}的{is_nick}！"
    await bot.send(event, repo_0)
    await asyncio.sleep(10)

    prep_list = await bot.get_group_member_list(group_id=group_id)
    prep_list = [prep.get("user_id", 114514) for prep in prep_list]

    lucky_user = choice(prep_list)
    lucky_user_info: dict = await bot.get_group_member_info(
        group_id=group_id, user_id=lucky_user
    )
    lucky_user_card = lucky_user_info["card"]
    if not lucky_user_card:
        lucky_user_card = lucky_user_info["nickname"]

    lucky_user_sex = lucky_user_info["sex"]

    data[str(lucky_user)] = MarryInfo(
        name=req_user_card, sex=is_nick, wife=user_id
    ).dict()
    data[user_id] = MarryInfo(
        name=lucky_user_card, sex=lucky_user_sex, wife=str(lucky_user)
    ).dict()
    Wife().save_marry_list(data)

    repo_1 = f"好欸！{lucky_user_card}成为了{req_user_card}的{is_nick}"
    await get_wife.finish(repo_1)


call_wife = Wife().on_command("老婆", "呼唤老婆/老公！", aliases={"老公", "老婆！", "老公！"})


@call_wife.handle([Cooldown(60)])
async def _call_wife(event: MessageEvent):
    user_id = event.get_user_id()

    data = Wife().load_marry_list()
    if user_id not in data:
        return

    wife = data[user_id].get("name", "ignore")
    sex = data[user_id].get("sex", "male")
    is_nick = "老公" if sex == "male" else "老婆"
    repo = f"你已经有{is_nick}啦！是{wife}噢~"
    await call_wife.finish(repo)


discard_wife = Wife().on_command("我要离婚", "离婚！")


@discard_wife.handle([Cooldown(60)])
async def _discard_wife(
    matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()
):
    user_id = event.get_user_id()

    data = Wife().load_marry_list()
    if user_id not in data:
        await discard_wife.finish("你还没对象呐...")

    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("is_disc", args)


@discard_wife.got("is_disc", "真的吗...（y/是）")
async def _deal_discard(
    bot: Bot, event: GroupMessageEvent, is_disc: str = ArgPlainText("is_disc")
):
    rd_list = ["y", "Y", "是", "确认", "对"]

    user_id = event.get_user_id()
    group_id = event.group_id
    if is_disc not in rd_list:
        user_info = await bot.get_group_member_info(
            group_id=group_id, user_id=int(user_id)
        )
        user_nickname = user_info["card"]
        if not user_nickname:
            user_nickname = user_info["nickname"]

        await discard_wife.finish(f"{user_nickname} 回心转意了！")

    group_info: dict = await bot.get_group_member_info(
        group_id=group_id, user_id=int(user_id)
    )
    user_card = group_info.get("card", "老婆")

    data = Wife().load_marry_list()

    discard_user_info = data[user_id]
    discard_user_card = discard_user_info["name"]
    discard_user_id = discard_user_info["wife"]

    data.pop(user_id)
    data.pop(discard_user_id)
    Wife().save_marry_list(data)
    repo = f"悲，{user_card}抛弃了{discard_user_card}..."
    await discard_wife.finish(repo)
