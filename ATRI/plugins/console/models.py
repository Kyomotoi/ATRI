from pydantic import BaseModel


class AuthData(BaseModel):
    token: str
    md5: str
    dead_time: int


class MessageDealerInfo(BaseModel):
    recv_msg: str
    deal_msg: str
    failed_deal_msg: str
    total_r_m: str
    total_d_m: str
    total_f_m: str
