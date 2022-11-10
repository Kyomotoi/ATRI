from typing import List
from pydantic import BaseModel


class BotConfig(BaseModel):
    host: str
    port: int
    debug: bool
    superusers: set
    nickname: set
    command_start: set
    command_sep: set
    session_expire_timeout: int
    access_token: str
    proxy: str
    request_timeout: int


class GoCQHTTPAccountList(BaseModel):
    uin: int
    password: str
    protocol: int


class WithGoCQHTTP(BaseModel):
    enabled: bool
    accounts: List[GoCQHTTPAccountList]
    download_domain: str
    download_version: str
    gocq_webui_username: str
    gocq_webui_password: str


class SauceNAO(BaseModel):
    key: str


class Setu(BaseModel):
    reverse_proxy: bool
    reverse_proxy_domain: str


class GeoIP(BaseModel):
    account_id: str
    license_key: str


class ConfigModel(BaseModel):
    ConfigVersion: str
    BotConfig: BotConfig
    WithGoCQHTTP: WithGoCQHTTP
    SauceNAO: SauceNAO
    Setu: Setu
    GeoIP: GeoIP


class RuntimeConfig(BaseModel):
    host: str
    port: int
    debug: bool
    superusers: set
    nickname: set
    onebot_access_token: str
    command_start: set
    command_sep: set
    session_expire_timeout: int
    gocq_accounts: list
    gocq_download_domain: str
    gocq_version: str
    gocq_webui_username: str
    gocq_webui_password: str
