import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

from ATRI.log import logger
from ATRI.exceptions import WriteError


SERVICE_DIR = Path('.') / 'ATRI' / 'data' / 'service'
PLUGIN_INFO_DIR = Path('.') / 'ATRI' / 'data' / 'service' / 'plugins'
os.makedirs(SERVICE_DIR, exist_ok=True)
os.makedirs(PLUGIN_INFO_DIR, exist_ok=True)

sleep = False

class Service:
    class ServiceInfo(BaseModel):
        name: str
        _type: str
        docs: Optional[str] = None
        command: Optional[list] = None
    
    @classmethod
    def register(
        cls,
        service_name: str,
        service_type: str,
        docs: Optional[str] = None,
        command: Optional[list] = None
    ) -> None:
        """
        启动时保存各个服务信息，便于后续网页控制台调用
        增强管理
        """
        file_name = f"{service_name}.function.json"
        path = SERVICE_DIR / file_name
        path.parent.mkdir(exist_ok=True, parents=True)
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        
        data = cls.ServiceInfo(
            name=service_name,
            _type=service_type,
            docs=docs,
            command=command
        )
        try:
            with open(path, 'w', encoding='utf-8') as target:
                target.write(
                    json.dumps(
                        data.dict(), indent=4
                    )
                )
        except WriteError:
            raise WriteError("Writing file failed!")
        else:
            pass
        
        # TODO: shitcode-style
        docs_judge = "N" if not docs else "Y"
        a = " "
        log_center = ""
        log_head = f"Success register service: [{service_name}]."
        log_suffix = f"Docs [{docs_judge}]. Type [{service_type}]"
        log_head_lenght = len(log_head)
        log_suffix_lenght = len(log_suffix)
        log_center_lenght = 120 - (
            log_head_lenght + log_suffix_lenght
        )
        for _ in range(log_center_lenght): log_center = log_center + a
        log_print = log_head + log_center + log_suffix
        logger.info(log_print)
    
    @staticmethod
    def is_dormant() -> bool:
        """
        为bot提供休眠，期间不会响应除了 superusers 以外的用户的信息
        触发在于 Rule
        """
        return False if sleep else True
    
    @staticmethod
    def control_dormant(_type: bool) -> None:
        """
        更改休眠状态
        """
        global sleep
        if _type:
            sleep = True
        else:
            sleep = False
