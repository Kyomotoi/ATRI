import json
import aiofiles
from typing import Optional

from ATRI.exceptions import InvalidWriteText

from . import SERVICE_PATH


class BanList:
    filename = 'banlist.service.json'
    path = SERVICE_PATH / filename
    path.parent.mkdir(exist_ok=True, parents=True)
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}

    @classmethod
    def get_banlist(cls) -> dict:
        return cls.data

    @classmethod
    def is_in_list(cls, user: Optional[str]) -> bool:
        return False if user in cls.data else True

    @classmethod
    async def add_list(cls, user: Optional[str]) -> None:
        try:
            cls.data[user] = user
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data, indent=4
                    )
                )
        except InvalidWriteText:
            raise InvalidWriteText('Writing file failed!')

    @classmethod
    async def del_list(cls, user: Optional[str]) -> None:
        try:
            del cls.data[user]
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data, indent=4
                    )
                )
        except InvalidWriteText:
            raise InvalidWriteText('List writing file failed!')
