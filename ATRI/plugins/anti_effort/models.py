from pydantic import BaseModel


class AntiEffortUserModel(BaseModel):
    user_id: int
    w_user_name: str
    w_user_id: str
    waka_url: str
    last_7_days_count: float
    recent_count: float
