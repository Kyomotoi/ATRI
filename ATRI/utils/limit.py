import datetime
from random import choice

from ATRI.config import Config
from ATRI.service import Service as sv
from .list import count_list, del_list_aim
from .apscheduler import scheduler, DateTrigger


exciting_user_temp = []
exciting_user = []
exciting_repo = [
    "歇歇8，。咱8能再快了",
    "太快惹，太快惹嗯",
    "你吼辣么快干什么！",
    "其实吧我觉得你这速度去d个vup挺适合",
    "我不接受！你太快了",
    "我有点担心，因为你太快了",
    "请稍等！您冲得太快了！"
]


def del_list(user: str) -> None:
    global exciting_user
    exciting_user = del_list_aim(exciting_user, user)


async def is_too_exciting(user: int, group: int,
                           times: int, repo: bool) -> bool:
    global exciting_user
    
    if user in exciting_user:
        if repo:
            await sv.NetworkPost.send_msg(user_id=user,
                                          group_id=group,
                                          message=choice(exciting_repo))
        return False
    else:
        if count_list(exciting_user_temp, user) == times:
            delta = datetime.timedelta(
                seconds=Config.BotSelfConfig.session_exciting_time)
            trigger = DateTrigger(
                run_date=datetime.datetime.now() + delta)
            
            scheduler.add_job(
                func=del_list,
                trigger=trigger,
                args=(user,),
                misfire_grace_time=1,
            )
            
            if repo:
                await sv.NetworkPost.send_msg(user_id=user,
                                              group_id=group,
                                              message=choice(exciting_repo))
            return False
        else:
            exciting_user_temp.append(user)
            return True
