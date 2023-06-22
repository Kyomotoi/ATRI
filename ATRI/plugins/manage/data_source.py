from typing import Dict
from pathlib import Path
from datetime import datetime

from nonebot import get_bot
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from ATRI.utils import FileDealer
from ATRI.service import ServiceTools
from ATRI.message import MessageBuilder
from ATRI.exceptions import load_error

from .models import RequestList


MANAGE_DIR = Path(".") / "data" / "plugins" / "manage"
MANAGE_DIR.mkdir(parents=True, exist_ok=True)


_TRACEBACK_FORMAT = (
    MessageBuilder("追踪ID：{trace_id}")
    .text("关键词：{prompt}")
    .text("时间：{time}")
    .text("{content}")
    .done()
)


class BotManager:
    async def __load_data(self, file_name: str) -> dict:
        path = MANAGE_DIR / file_name
        dealer = FileDealer(path)
        if not path.is_file():
            await dealer.write_json(dict())

        try:
            data = dealer.json()
        except Exception:
            data = dict()
        return data

    async def __store_data(self, file_name: str, data: dict) -> None:
        path = MANAGE_DIR / file_name
        dealer = FileDealer(path)
        if not path.is_file():
            await dealer.write_json(dict())

        await dealer.write_json(data)

    async def __load_block_group(self) -> dict:
        return await self.__load_data("block_group.json")

    async def __store_block_group(self, data: dict) -> None:
        await self.__store_data("block_group.json", data)

    async def __load_block_user(self) -> dict:
        return await self.__load_data("block_user.json")

    async def __store_block_user(self, data: dict) -> None:
        await self.__store_data("block_user.json", data)

    async def load_friend_req(self) -> RequestList:
        return RequestList.parse_obj(await self.__load_data("friend_add.json"))

    async def store_friend_req(self, data: dict) -> None:
        await self.__store_data("friend_add.json", data)

    async def load_group_req(self) -> RequestList:
        return RequestList.parse_obj(await self.__load_data("group_invite.json"))

    async def store_group_req(self, data: dict) -> None:
        await self.__store_data("group_invite.json", data)

    async def block_group(self, group_id: str) -> None:
        data = await self.__load_block_group()
        data[group_id] = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            await self.__store_block_group(data)
        except Exception:
            raise Exception("写入文件时失败")

    async def unblock_group(self, group_id: str) -> None:
        data = await self.__load_block_group()
        if group_id not in data:
            raise Exception("群不存在于封禁名单")

        try:
            data.pop(group_id)
            await self.__store_block_group(data)
        except Exception:
            raise Exception("写入文件时失败")

    async def block_user(self, user_id: str) -> None:
        data = await self.__load_block_user()
        data[user_id] = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            await self.__store_block_user(data)
        except Exception:
            raise Exception("写入文件时失败")

    async def unblock_user(self, user_id: str) -> None:
        data = await self.__load_block_user()
        if user_id not in data:
            raise Exception("用户不存在于封禁名单")

        try:
            data.pop(user_id)
            await self.__store_block_user(data)
        except Exception:
            raise Exception("写入文件时失败")

    def toggle_global_service(self, service: str) -> bool:
        serv = ServiceTools(service)
        try:
            data = serv.load_service()
        except Exception as e:
            error_msg = str(e)
            raise Exception(error_msg)

        data.enabled = not data.enabled
        serv.save_service(data)
        return data.enabled

    def toggle_group_service(self, service: str, event) -> bool:
        if isinstance(event, GroupMessageEvent):
            group_id = str(event.group_id)
            serv = ServiceTools(service)
            try:
                data = serv.load_service()
            except Exception as e:
                error_msg = str(e)
                raise Exception(error_msg)

            if group_id in data.disable_group:
                data.disable_group.remove(group_id)
                result = True
            else:
                data.disable_group.append(group_id)
                result = False
            serv.save_service(data)
            return result
        raise Exception("该功能只能在群聊中使用")

    def toggle_user_service(self, service: str, user_id: str) -> bool:
        serv = ServiceTools(service)
        try:
            data = serv.load_service()
        except Exception as e:
            error_msg = str(e)
            raise Exception(error_msg)

        if user_id in data.disable_user:
            data.disable_user.remove(user_id)
            result = True
        else:
            data.disable_user.append(user_id)
            result = False
        serv.save_service(data)
        return result

    async def track_error(self, trace_id: str) -> str:
        try:
            data = load_error(trace_id)
        except Exception:
            raise Exception("未找到对应ID的信息")

        return _TRACEBACK_FORMAT.format(
            trace_id=data.track_id,
            prompt=data.prompt,
            time=data.time,
            content=data.content,
        )

    def __get_bot(self) -> Bot:
        try:
            return get_bot()
        except Exception:
            raise Exception("无法获取 bot 实例")

    async def apply_friend_req(self, code: str) -> None:
        bot = self.__get_bot()
        try:
            await bot.call_api("set_friend_add_request", flag=code, approve=True)
        except Exception:
            raise Exception("同意失败，请尝试手动同意")
        raw_data = await self.load_friend_req()
        data = raw_data.data
        data.pop(code)
        raw_data.data = data
        await self.store_friend_req(raw_data.dict())

    async def reject_friend_req(self, code: str) -> None:
        bot = self.__get_bot()
        try:
            await bot.call_api("set_friend_add_request", flag=code, approve=False)
        except Exception:
            raise Exception("拒绝失败，请尝试手动拒绝")
        raw_data = await self.load_friend_req()
        data = raw_data.data
        data.pop(code)
        raw_data.data = data
        await self.store_friend_req(raw_data.dict())

    async def apply_group_req(self, code: str) -> None:
        bot = self.__get_bot()
        try:
            await bot.call_api(
                "set_group_add_request", flag=code, sub_type="invite", approve=True
            )
        except Exception:
            raise Exception("同意失败，请尝试手动同意")
        raw_data = await self.load_group_req()
        data = raw_data.data
        data.pop(code)
        raw_data.data = data
        await self.store_group_req(raw_data.dict())

    async def reject_group_req(self, code: str) -> None:
        bot = self.__get_bot()
        try:
            await bot.call_api(
                "set_group_add_request", flag=code, sub_type="invite", approve=False
            )
        except Exception:
            raise Exception("拒绝失败，请尝试手动拒绝")
        raw_data = await self.load_group_req()
        data = raw_data.data
        data.pop(code)
        raw_data.data = data
        await self.store_group_req(raw_data.dict())
