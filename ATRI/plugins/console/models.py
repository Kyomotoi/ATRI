from pydantic import BaseModel


class AuthData(BaseModel):
    token: str


class PlatformRuntimeInfo(BaseModel):
    stat_msg: str
    cpu_percent: str
    mem_percent: str
    disk_percent: str
    inte_send: str
    inte_recv: str
    boot_time: str


class BotRuntimeInfo(BaseModel):
    cpu_percent: str
    mem_percent: str
    bot_run_time: str


class MessageDealerInfo(BaseModel):
    recv_msg: str
    deal_msg: str
    failed_deal_msg: str
    total_r_m: str
    total_d_m: str
    total_f_m: str


class ServiceInfo(BaseModel):
    service_name: str
    service_docs: str
    is_enabled: bool
    disable_user: list
    disable_group: list
