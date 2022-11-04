from typing import Union

from nonebot.adapters.onebot.v11 import Bot as _Bot
from nonebot.adapters.onebot.v11 import Message

from ATRI.permission import MASTER_LIST


class Bot(_Bot):
    async def send_to_master(self, message: Union[str, Message]):
        for m in MASTER_LIST:
            await self.send_private_msg(user_id=m, message=message)
