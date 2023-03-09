from pydantic import BaseModel


class Response(BaseModel):
    status: int
    detail: str
    data: dict


class StatusInfo(BaseModel):
    platform: dict
    cpu: dict
    mem: dict
    disk: dict
    net: dict
