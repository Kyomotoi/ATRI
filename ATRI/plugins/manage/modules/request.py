import re
import json
from pathlib import Path

from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.exceptions import ReadFileError, FormatError


ESSENTIAL_DIR = Path(".") / "ATRI" / "data" / "database" / "essential"


__doc__ = """
查看好友/群申请列表
权限组：维护者
用法：
  查看申请列表
"""

req_list = sv.on_command(cmd="申请列表", docs=__doc__, permission=SUPERUSER)


@req_list.handle()
async def _req_list(bot: Bot, event: MessageEvent) -> None:
    path_f = ESSENTIAL_DIR / "request_friend.json"
    path_g = ESSENTIAL_DIR / "request_group.json"
    data_f, data_g = dict()
    try:
        data_f = json.loads(path_f.read_bytes())
    except ReadFileError:
        msg_f = "[读取文件失败]"
    try:
        data_g = json.loads(path_g.read_bytes())
    except ReadFileError:
        msg_g = "[读取文件失败]"

    msg_f = str()
    for i in data_f.keys():
        msg_f += f"{i} | {data_f[i]['user_id']} | {data_f[i]['comment']}\n"

    msg_g = str()
    for i in data_g.keys():
        msg_g += f"{i} | {data_g[i]['sub_type']} | {data_g[i]['user_id']} | {data_g[i]['comment']}\n"

    msg = "好友/群申请列表如下：\n" "· 好友：\n" f"{msg_f}" "· 群：\n" f"{msg_g}"
    await req_list.finish(msg)


req_deal = sv.on_regex(r"(同意|拒绝)(好友|群)申请", permission=SUPERUSER)


@req_deal.handle()
async def _req_deal(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    arg = re.findall(r"(同意|拒绝)(好友|群)申请", msg[0])[0]
    app = arg[0]
    _type = arg[1]

    if not msg[1]:
        await req_deal.finish(f"正确用法！速看\n{app}{_type}申请 (reqid)")

    reqid = msg[1]
    if app == "同意":
        if _type == "好友":
            try:
                await bot.set_friend_add_request(flag=reqid, approve=True)
                await req_deal.finish("完成~！已同意申请")
            except FormatError:
                await req_deal.finish("请检查输入的值是否正确——！")
        elif _type == "群":
            path = ESSENTIAL_DIR / "request_group.json"
            data_g = dict()
            try:
                data_g = json.loads(path.read_bytes())
            except FileExistsError:
                await req_deal.finish("读取群数据失败，可能并没有请求...")

            try:
                await bot.set_group_add_request(
                    flag=reqid, sub_type=data_g[reqid]["sub_type"], approve=True
                )
                await req_deal.finish("完成~！已同意申请")
            except FormatError:
                await req_deal.finish("请检查输入的值是否正确——！")
        else:
            await req_deal.finish("请检查输入的值是否正确——！")
    elif app == "拒绝":
        if _type == "好友":
            try:
                await bot.set_friend_add_request(flag=reqid, approve=False)
                await req_deal.finish("完成~！已拒绝申请")
            except FormatError:
                await req_deal.finish("请检查输入的值是否正确——！")
        elif _type == "群":
            path = ESSENTIAL_DIR / "request_group.json"
            data_g = dict()
            try:
                data_g = json.loads(path.read_bytes())
            except FileExistsError:
                await req_deal.finish("读取群数据失败，可能并没有请求...")

            try:
                await bot.set_group_add_request(
                    flag=reqid, sub_type=data_g[reqid]["sub_type"], approve=False
                )
                await req_deal.finish("完成~！已拒绝申请")
            except FormatError:
                await req_deal.finish("请检查输入的值是否正确——！")
        else:
            await req_deal.finish("请检查输入的值是否正确——！")
    else:
        await req_deal.finish("请检查输入的值是否正确——！")
