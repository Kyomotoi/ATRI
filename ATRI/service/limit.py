import json
import aiofiles

from ATRI.exceptions import WriteError
from . import SERVICE_DIR


class Limit:
    
    file_name = "limit.service.json"
    path = SERVICE_DIR / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}
    
    @classmethod
    def _filling_service(cls, service, group: int = None):
        # Determine whether the service exists in global variables.
        if service not in cls.data["global"]:
            cls.data["global"][service] = True
        # Similary, for group.
        if service not in cls.data[group]:
            cls.data[group][service] = True
        
    
    @classmethod
    def get_service(cls) -> dict:
        return cls.data
    
    @classmethod
    async def auth_service(
        cls, service: str, group: int = None) -> bool:
        cls.data.setdefault("global", {})
        cls.data.setdefault(group, {})
        cls._filling_service(service, group)
        
        try:
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data
                    )
                )
        except WriteError:
            raise WriteError("Writing file failed!")
        
        if cls.data["global"][service]:
            return True if cls.data[group][service] else False
        else:
            return False
    
    @classmethod
    async def control_service(
        cls,
        service: str,
        status: bool,
        group: int = None
    ) -> None:
        cls._filling_service(service, group)
        
        if group:
            cls.data[group][service] = status
        else:
            cls.data["global"][service] = status
        
        try:
            async with aiofiles.open(
                cls.path, 'w', encoding='utf-8') as target:
                await target.write(
                    json.dumps(
                        cls.data
                    )
                )
        except WriteError:
            raise WriteError("Writing file failed!")
