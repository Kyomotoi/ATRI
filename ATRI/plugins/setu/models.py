from typing import List
from pydantic import BaseModel


class Urls(BaseModel):
    original: str


class Datum(BaseModel):
    pid: int
    p: int
    uid: int
    title: str
    author: str
    r18: bool
    width: int
    height: int
    tags: List[str]
    ext: str
    aiType: int
    uploadDate: int
    urls: Urls


class LoliconResponse(BaseModel):
    error: str
    data: List[Datum]


class SetuInfo(BaseModel):
    title: str
    pid: int
    url: str
