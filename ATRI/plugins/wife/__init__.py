import asyncio
from random import choice
from pydantic import BaseModel

from nonebot.permission import USER
from nonebot.rule import Rule
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent, Message

from ATRI.utils.limit import FreqLimiter
from .data_source import Wife


_tietie_flmt = FreqLimiter(600)


tietie_superuser = Wife().on_message("只与维护者贴贴w", rule=Rule(), permission=SUPERUSER, block=False)

@tietie_superuser.handle()
async def _tietie_superuser(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _tietie_flmt.check(user_id):
        await tietie_superuser.finish()
    
    result = Wife().to_superuser(user_id)
    _tietie_flmt.start_cd(user_id)
    await tietie_superuser.finish(Message(result))


_wife_flmt = FreqLimiter(10)

class MarryInfo(BaseModel):
    name: str
    sex: str
    wife: str


get_wife = Wife().on_command("抽老婆", "随机选择一位幸运裙友成为老婆！")

@get_wife.handle()
async def _get_wife(bot: Bot, event: GroupMessageEvent):
    user_id = event.get_user_id()
    if not _wife_flmt.check(user_id):
        await get_wife.finish()
    
    group_id = event.group_id
    req_user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=int(user_id))
    req_user_card = req_user_info["card"]
    req_user_sex = req_user_info["sex"]
    is_nick = "老公" if req_user_sex == "male" else "老婆"
    
    repo_0 = (
        "现在咱将随机抽取一位幸运裙友\n"
        f"成为{req_user_card}的{is_nick}！"
    )
    await bot.send(event, repo_0)
    await asyncio.sleep(10)
    
    prep_list = await bot.get_group_member_list(group_id=group_id)
    prep_list = [prep.get("user_id", 114514) for prep in prep_list]
    
    lucky_user = choice(prep_list)
    lucky_user_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=lucky_user)
    lucky_user_card = lucky_user_info["card"]
    lucky_user_sex = lucky_user_info["sex"]
    
    data = Wife().load_marry_list()
    data[lucky_user] = MarryInfo(
        name=req_user_card,
        sex=is_nick,
        wife=user_id
    ).dict()
    data[user_id] = MarryInfo(
        name=lucky_user_card,
        sex=lucky_user_sex,
        wife=lucky_user
    ).dict()
    Wife().save_marry_list(data)
    
    repo_1 = f"好欸！{lucky_user_card}成为了{req_user_card}的{is_nick}"
    _wife_flmt.start_cd(user_id)
    await get_wife.finish(repo_1)


_call_wife_flmt = FreqLimiter(60)


call_wife = Wife().on_command("老婆", "呼唤老婆/老公！", aliases={"老公", "老婆！", "老公！"}, permission=USER("114514"))

@call_wife.handle()
async def _call_wife(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _wife_flmt.check(user_id):
        await call_wife.finish()
    
    data = Wife().load_marry_list()
    if user_id not in data:
        return
    
    wife = data[user_id].get("wife", "ignore")
    sex = data[user_id].get("sex", "male")
    is_nick = "老公" if sex == "male" else "老婆"
    repo = f"你已经有{is_nick}啦！是{wife}噢~"
    _call_wife_flmt.start_cd(user_id)
    await call_wife.finish(repo)


discard_wife = Wife().on_command("我要离婚", "离婚！")

@discard_wife.handle()
async def _discard_wife(bot: Bot, event: GroupMessageEvent):
    user_id = event.get_user_id()
    if not _wife_flmt.check(user_id):
        await discard_wife.finish()
    
    await bot.send(event, "真的吗...（y/是）")
    msg = str(event.message).strip()
    rd_list = ["y", "Y", "是", "确认", "对"]
    if msg not in rd_list:
        await discard_wife.finish("")
    
    group_id = event.group_id
    group_info: dict = await bot.get_group_member_info(group_id=group_id, user_id=int(user_id))
    user_card = group_info.get("card", "老婆")
    
    data = Wife().load_marry_list()
    if user_id not in data:
        await discard_wife.finish("你还没对象呐...")
    
    discard_user_info = data[user_id]
    discard_user_card = discard_user_info["name"]
    discard_user_id = discard_user_info["wife"]
    
    data.pop(user_id)
    data.pop(discard_user_id)
    Wife().save_marry_list(data)
    repo = f"悲，{user_card}抛弃了{discard_user_card}..."
    _wife_flmt.start_cd(user_id)
    await discard_wife.finish(repo)
