import datetime
from random import choice

from ATRI.service import Service as sv
from .list import count_list, del_list_aim
from .apscheduler import scheduler, DateTrigger


exciting_user_temp = []
exciting_user = []


def del_list(user: str) -> None:
    global exciting_user
    exciting_user = del_list_aim(exciting_user, user)


def is_too_exciting(
    user: int, times: int, seconds: float = 0, hours: float = 0, days: float = 0
) -> bool:
    global exciting_user

    if user in exciting_user:
        return False
    else:
        if count_list(exciting_user_temp, user) == times:
            delta = datetime.timedelta(seconds=seconds, hours=hours, days=days)
            trigger = DateTrigger(run_date=datetime.datetime.now() + delta)

            scheduler.add_job(
                func=del_list,
                trigger=trigger,
                args=(user,),
                misfire_grace_time=1,
            )
            return False
        else:
            exciting_user_temp.append(user)
            return True
