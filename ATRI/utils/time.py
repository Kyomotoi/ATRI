from datetime import datetime


def now_time() -> float:
    """获取当前小时整数"""
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now
