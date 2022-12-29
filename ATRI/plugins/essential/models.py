from pydantic import BaseModel


class RequestInfo(BaseModel):
    user_id: str
    comment: str
    time: str
