import json
import aiofiles
from typing import Optional

from ATRI.exceptions import InvalidWriteText

from . import SERVICE_PATH


class Switch:
    filename = 'switch.service.json'
    path = SERVICE_PATH / filename
    path.parent.mkdir(exist_ok=True, parents=True)
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}

    @classmethod
    def get_service(cls) -> dict:
        return cls.data

    @classmethod
    async def auth_service(
        cls, service: str, group: Optional[int] = None) -> bool:
        cls.data.setdefault('global', {})
        cls.data.setdefault(group, {})
        if service not in cls.data['global']:
            cls.data['global'][service] = True
        if service not in cls.data[group]:
            cls.data[group][service] = True
        try:
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data, indent=4
                    )
                )
        except InvalidWriteText:
            raise InvalidWriteText('Writing file failed!')
        else:
            pass

        if cls.data['global'][service]:
            return True if cls.data[group][service] else False
        else:
            return False

    @classmethod
    async def control_service(cls, service: str, _type: bool,
                        group: Optional[str]) -> None:
        if service not in cls.data:
            cls.data['global'][service] = True
            cls.data[group][service] = True
            try:
                async with aiofiles.open(
                    cls.path, 'w', encoding='utf-8') as target:
                    await target.write(
                        json.dumps(
                            cls.data, indent=4
                        )
                    )
            except InvalidWriteText:
                raise InvalidWriteText('Writing file failed!')
        if group:
            cls.data[group][service] = _type
        else:
            cls.data['global'][service] = _type
        try:
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data, indent=4
                    )
                )
        except InvalidWriteText:
            raise InvalidWriteText('Writing file failed!')
