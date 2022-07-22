from pydantic import BaseModel


class AntiEffortModel(BaseModel):
    update_time: str
    data: list


class AntiEffortUserModel(BaseModel):
    user_id: int
    user_nickname: str
    w_user_id: str
    waka_url: str
    last_7_days_count: float
    recent_count: float
