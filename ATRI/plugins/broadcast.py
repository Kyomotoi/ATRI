import json
import random
import asyncio
from pathlib import Path

from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent


from ATRI.service import Service
from ATRI.rule import to_bot


BC_PATH = Path(".") / "data" / "database" / "broadcast"
BC_PATH.mkdir(parents=True, exist_ok=True)


_BROADCAST_BACK = """
广播报告：
信息：{msg}
预计推送个数（群）：{len_g}
成功：{su_g}
失败：{fl_g}
失败列表：{f_g}
""".strip()


class BroadCast(Service):
    def __init__(self):
        Service.__init__(self, "广播", "向bot所在的所有群发送信息", True, to_bot())

    @staticmethod
    def load_rej_list() -> list:
        data = list()
        path = BC_PATH / "rej_list.json"
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps(data))
            return data

        return json.loads(path.read_bytes())

    @classmethod
    def store_rej_list(cls, data: list):
        path = BC_PATH / "rej_list.json"
        if not path.is_file():
            cls.load_rej_list()

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data))


caster = BroadCast().on_command(
    "广播", "向bot所在的所有群发送信息，有防寄延迟", aliases={"bc"}, permission=SUPERUSER
)


@caster.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("bc_msg", args)


@caster.got("bc_msg", "想要咱群发什么呢？")
async def _(bot: Bot, event: MessageEvent, s_msg: str = ArgPlainText("bc_msg")):
    w_group = await bot.get_group_list()

    await bot.send(event, "正在推送...（每个群延迟1～3s）")

    w_msg = f" 来自维护者的信息：\n{s_msg}"

    su_g = list()
    fl_g = list()
    for i in w_group:
        group_id = i["group_id"]
        try:
            await bot.send_group_msg(group_id=group_id, message=w_msg)
            su_g.append(group_id)
        except:
            fl_g.append(group_id)

        await asyncio.sleep(random.randint(2, 3))

    repo_msg = _BROADCAST_BACK.format(
        msg=s_msg,
        len_g=len(w_group),
        su_g=su_g,
        fl_g=fl_g,
        f_g="、".join(map(str, fl_g)),
    )
    await caster.finish(repo_msg)


rej_broadcast = BroadCast().on_command(
    "拒绝广播", "拒绝来自开发者的广播推送", permission=GROUP_OWNER | GROUP_ADMIN
)


@rej_broadcast.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = str(event.group_id)

    rej_g = BroadCast().load_rej_list()
    if group_id in rej_g:
        await rej_broadcast.finish("本群已在推送黑名单内辣！")
    else:
        rej_g.append(group_id)
        BroadCast().store_rej_list(rej_g)
        await rej_broadcast.finish("完成～！已将本群列入推送黑名单")


@rej_broadcast.handle()
async def _(event: PrivateMessageEvent):
    await rej_broadcast.finish("该功能仅在群聊中触发...")


acc_broadcast = BroadCast().on_command(
    "接受广播", "接受来自开发者的广播推送", permission=GROUP_OWNER | GROUP_ADMIN
)


@acc_broadcast.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = str(event.group_id)

    rej_g = BroadCast().load_rej_list()
    if group_id in rej_g:
        rej_g.remove(group_id)
        BroadCast().store_rej_list(rej_g)
        await rej_broadcast.finish("已将本群移除推送黑名单！")
    else:
        await rej_broadcast.finish("本群不在推送黑名单里呢...")


@acc_broadcast.handle()
async def _(event: PrivateMessageEvent):
    await rej_broadcast.finish("该功能仅在群聊中触发...")
