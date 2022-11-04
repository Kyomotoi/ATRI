from pydantic import BaseModel


class PlatformRuntimeInfo(BaseModel):
    cpu_percent: str
    mem_percent: str
    disk_percent: str
    net_sent: str
    net_recv: str
    boot_time: str


class BotRuntimeInfo(BaseModel):
    cpu_percent: str
    mem_percent: str
    run_time: str


class RuntimeInfo(BaseModel):
    status_message: str
    platform_info: PlatformRuntimeInfo
    bot_info: BotRuntimeInfo


class ServiceInfo(BaseModel):
    service: str
    docs: str
    permission: list
    cmd_list: dict
    enabled: bool
    only_admin: bool
    disable_user: list
    disable_group: list


class BlockInfo(BaseModel):
    user: dict
    group: dict
