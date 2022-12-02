from pydantic import BaseModel


class SetuInfo(BaseModel):
    title: str
    pid: str
