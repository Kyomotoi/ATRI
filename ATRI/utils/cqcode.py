import re
from typing import Optional

from ATRI.service import Service as sv


tencent_gchat_url = "gchat.qpic.cn"
noob_code = ["record", "video", "music", "xml", "json"]


async def coolq_code_check(cq_code: str,
                     user: Optional[int] = None,
                     group: Optional[int] = None):
    _type = re.findall(r"CQ:(.*?),", cq_code)
    for i in _type:
        if i == "image":
            result = re.findall(r"url=(.*?)]", cq_code)
            url = "" if not result else result[0]
            if tencent_gchat_url not in url:
                msg = "你注你🐎呢"
                await sv.NetworkPost.send_msg(user_id=user,
                                              group_id=group,
                                              message=msg)
            else:
                return True
        elif i in noob_code:
            return False
        else:
            return True