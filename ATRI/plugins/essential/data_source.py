from typing import Union

from ATRI.utils import MessageChecker
from ATRI.message import MessageSegment


def recall_msg_dealer(message: Union[dict, str]) -> str:
    if isinstance(message, str):
        return message
    
    cache_list = list()
    for i in message:
        _type = i.get("type")
        _data = i.get("data")
        if _type == "text":
            cache_list.append(_data["text"])
        elif _type == "image":
            url = _data["url"]
            check = MessageChecker(url).check_image_url
            if check:
                cache_list.append(MessageSegment.image(url))
            else:
                cache_list.append(f"[该图片可能包含危险内容, 源url: {url}]")
        elif _type == "face":
            cache_list.append(MessageSegment.face(_data["id"]))
        else:
            cache_list.append(f"[未知类型信息: {_data}]")
    
    return str().join(map(str, cache_list))