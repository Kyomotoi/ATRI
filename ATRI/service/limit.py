import json
from pathlib import Path
from typing import Optional

from ATRI.utils.file import write_file
from . import SERVICE_DIR


class Limit:
    @staticmethod
    def _get_file(group: Optional[int] = None) -> Path:
        file_name = f"{group}.service.json"
        LIMIT_DIR = SERVICE_DIR / "limit"
        path = LIMIT_DIR / file_name
        
        if not LIMIT_DIR.exists():
            LIMIT_DIR.mkdir()
        return path
    
    @classmethod
    def _read_file(cls, group: Optional[int] = None) -> dict:
        try:
            data = json.loads(cls._get_file(group).read_bytes())
        except:
            data = {}
        return data

    @classmethod
    async def auth_service(cls, service: str, group: Optional[int] = None) -> bool:
        data = cls._read_file(group)
        if service not in data:
            data[service] = True
            await write_file(cls._get_file(group), json.dumps(data))
        
        if data[service]:
            return True
        else:
            return False
    
    @classmethod
    async def control_service(
        cls,
        service: str,
        status: bool,
        group: Optional[int] = None
    ) -> None:
        data = cls._read_file(group)
        if service not in data:
            data[service] = True
            await write_file(cls._get_file(group), json.dumps(data))
        
        data[service] = status
        await write_file(cls._get_file(group), json.dumps(data))
