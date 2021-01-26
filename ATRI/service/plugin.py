import json
from typing import Optional
from pydantic import BaseModel

from ATRI.log import logger
from ATRI.exceptions import InvalidWriteText

from . import SERVICE_PATH


class Plugin:
    class PluginInfo(BaseModel):
        name: str
        _type: str
        docs: Optional[str] = None
        command: list
    
    @classmethod
    def register(cls, plugin_name: str, _type: str,
                        doc: Optional[str] = None,
                        command: Optional[list] = None) -> None:
        filename = f'{plugin_name}.plugins.json'
        path = SERVICE_PATH / 'plugins' / filename
        path.parent.mkdir(exist_ok=True, parents=True)
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        
        data = cls.PluginInfo(
            name=plugin_name,
            _type=_type,
            docs=doc,
            command=command
        )
        try:
            with open(path, 'w', encoding='utf-8') as target:
                target.write(
                    json.dumps(
                        data.dict(), indent=4
                    )
                )
        except InvalidWriteText:
            raise InvalidWriteText('Writing file failed!')
        else:
            pass
        docs_judge = "N" if not doc else "Y"

        a = ' '
        log_center = ''
        log_head = f"Success register plugin: [{plugin_name}]."
        log_suffix = f"Docs [{docs_judge}]. Type [{_type}]"
        log_head_lenght = len(log_head)
        log_suffix_lenght = len(log_suffix)
        log_center_lenght = 120 - (
            log_head_lenght + log_suffix_lenght
        )
        for _ in range(log_center_lenght): log_center = log_center + a
        log_print = log_head + log_center + log_suffix
        logger.info(log_print)
