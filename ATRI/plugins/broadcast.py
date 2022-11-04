import json
import random
import asyncio

from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, GroupMessageEvent

from ATRI.rule import to_bot
from ATRI.service import Service
from ATRI.utils import FileDealer
from ATRI.permission import ADMIN, MASTER
from ATRI.message import MessageBuilder


_BROADCAST_REPO_FORMAT = (
    MessageBuilder("广播报告:")
    .text("信息: {msg}")
    .text("预计推送群:{len_group} 个")
    .text("成功: {success_group} 失败: {failed_group}")
    .text("失败群列表:")
    .text("{failed_group_list}")
    .done()
)


async def __load_reject_list() -> list:
    path = plugin.get_path() / "rej_list.json"
    file = FileDealer(path)
    if not path.is_file():
        await file.write(list())
        return list()

    return list(file.json())


async def __store_reject_list(data: list) -> None:
    path = plugin.get_path() / "rej_list.json"
    file = FileDealer(path)
    if not path.is_file():
        await __load_reject_list()

    await file.write(json.dumps(data))


plugin = Service("广播").document("向bot所在的所有群发送信息").rule(to_bot())


caster = plugin.on_command("广播", "向bot所在的群发送信息", aliases={"/bc"}, permission=MASTER)


@caster.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("bc_msg", args)


@caster.got("bc_msg", prompt="需要咱广播啥呢")
async def _(bot: Bot, event: MessageEvent, msg: str = ArgPlainText("bc_msg")):
    group_list = await bot.get_group_list()
    if not group_list:
        await caster.finish("你还没让咱加入任何群呢...")

    await caster.send("正在推送...(每群延迟2-4s)")

    bc_msg = Message(f"来自维护者的消息:\n{msg}")

    success_group = list()
    failed_group = list()
    for i in group_list:
        group_id = i["group_id"]
        try:
            await bot.send_group_msg(group_id=group_id, message=bc_msg)
            success_group.append(group_id)
        except Exception:
            failed_group.append(group_id)

        await asyncio.sleep(random.randint(2, 4))

    result = _BROADCAST_REPO_FORMAT.format(
        msg=bc_msg,
        len_group=len(group_list),
        success_group=len(success_group),
        failed_group=len(failed_group),
        failed_group_list=", ".join(map(str, failed_group)),
    )
    await caster.finish(Message(result))


reject_bc = plugin.on_command("拒绝广播", "拒绝来自维护者的信息推送", permission=ADMIN)


@reject_bc.handle()
async def _(event: GroupMessageEvent):
    group_id = str(event.group_id)

    reject_list = await __load_reject_list()
    if group_id in reject_list:
        await reject_bc.finish("本群拒绝过啦~")
    else:
        reject_list.append(group_id)
        await __store_reject_list(reject_list)
        await reject_bc.finish("完成!")


accept_bc = plugin.on_command("接受广播", "接受来自维护者的信息推送", permission=ADMIN)


@accept_bc.handle()
async def _(event: GroupMessageEvent):
    group_id = str(event.group_id)

    reject_list = await __load_reject_list()
    if group_id in reject_list:
        reject_list.remove(group_id)
        await __store_reject_list(reject_list)
        await accept_bc.finish("完成!")
    else:
        await accept_bc.finish("本群未拒绝广播呢...")
