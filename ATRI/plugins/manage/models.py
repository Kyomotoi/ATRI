from typing import Dict
from pydantic import BaseModel


class RequestInfo(BaseModel):
    user_id: str
    comment: str
    time: str


class RequestList(BaseModel):
    data: Dict[str, RequestInfo]


class NonebotPluginInfo(BaseModel):
    module_name: str
    project_link: str
    name: str
    desc: str
    author: str
    homepage: str
    tags: list
    is_official: bool
