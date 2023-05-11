from typing import Literal
from pydantic import BaseModel, create_model

from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.event import (
    Sender,
    GroupMessageEvent,
    PrivateMessageEvent,
)


def escape_text(s: str, *, escape_comma: bool = True) -> str:
    s = s.replace("&", "&amp;").replace("[", "&#91;").replace("]", "&#93;")
    if escape_comma:
        s = s.replace(",", "&#44;")
    return s


class CommonFields(BaseModel):
    time: int = 1000000
    self_id: int = 1
    post_type: str = "message"
    sub_type: str = "normal"
    message_id: int = 1
    message: Message = Message("test")
    original_message: Message = Message("test")
    raw_message: str = "test"
    font: int = 0
    to_me: bool = False


class GroupMessageEventFields(BaseModel):
    user_id: int = 1145141919
    message_type: Literal["group"] = "group"
    group_id: int = 10000
    sender: Sender = Sender(card="", nickname="test", role="member")


class PrivateMessageEventFields(BaseModel):
    sub_type: str = "friend"
    user_id: int = 1145141919
    message_type: Literal["private"] = "private"
    sender: Sender = Sender(nickname="test")


def fake_event(event_cls, upgrade_cls: BaseModel, **field):
    _Fake = create_model("_Fake", __base__=event_cls)

    class FakeEvent(_Fake):
        __fields__ = {
            **CommonFields.__fields__,
            **upgrade_cls.__fields__,
        }

        class Config:
            extra = "forbid"

    return FakeEvent(**field)


def group_message_event(**field) -> GroupMessageEvent:
    if "message" in field:
        field.update({"original_message": field["message"]})
        field.update({"raw_message": str(field["message"])})
    return fake_event(GroupMessageEvent, GroupMessageEventFields, **field)  # type: ignore


def private_message_event(**field) -> PrivateMessageEvent:
    if "message" in field:
        field.update({"original_message": field["message"]})
        field.update({"raw_message": str(field["message"])})
    return fake_event(PrivateMessageEvent, PrivateMessageEventFields, **field)  # type: ignore
