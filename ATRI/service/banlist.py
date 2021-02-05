import json
import aiofiles
from typing import Optional

from ATRI.exceptions import WriteError
from . import SERVICE_DIR


class BanSystem:
    
    file_name = "banlist.service.json"
    path = SERVICE_DIR / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}
    
    @classmethod
    def get_list(cls) -> dict:
        return cls.data
    
    @classmethod
    def is_in_list(cls, user: Optional[str]) -> bool:
        return False if user in cls.data else True

    @classmethod
    async def add_to_list(cls, user: Optional[str]) -> None:
        cls.data[user] = user
        try:
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data, indent=4
                    )
                )
        except WriteError:
            raise WriteError("Writing file failed!")
    
    @classmethod
    async def del_from_list(cls, user: Optional[str]) -> None:
        del cls.data[user]
        try:
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data, indent=4
                    )
                )
        except WriteError:
            raise WriteError("Writing file failed!")
