import time
import pytz
import functools
from threading import RLock
from collections import defaultdict, deque
from datetime import datetime, timedelta


class LimitBucket:
    """
    限制某功能运行中某段在一定速率下
    """

    def __init__(self, capacity, fill_rate, is_lock: bool = False) -> None:
        """
        :param capacity: 容量总数
        :param fill_rate: 重新装填速率（单位：秒）
        """
        self._capacity = float(capacity)
        self._tokens = float(capacity)
        self._fill_rate = float(fill_rate)
        self._last_time = time()
        self._is_lock = is_lock
        self._lock = RLock()

    def _get_cur_tokens(self):
        if self._tokens < self._capacity:
            now = time()
            delta = self._fill_rate * (now - self._last_time)
            self._tokens = min(self._capacity, self._tokens + delta)
            self._last_time = now
        return self._tokens

    def get_cur_tokens(self):
        if self._is_lock:
            with self._lock:
                return self._get_cur_tokens()
        else:
            return self._get_cur_tokens()

    def _consume(self, tokens) -> bool:
        if tokens <= self.get_cur_tokens():
            self._tokens -= tokens
            return True
        return False

    def consume(self, tokens):
        if self._is_lock:
            with self._lock:
                return self._consume(tokens)
        else:
            return self._consume(tokens)


class RateLimiting:
    """
    限制该功能全体速率
    """

    def __init__(self, max_calls, period=1.0):
        if period <= 0:
            raise ValueError("Rate limiting period should be > 0")
        if max_calls <= 0:
            raise ValueError("Rate limiting number of calls should be > 0")

        self.calls = deque()

        self.period = period
        self.max_calls = max_calls

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapped

    def __enter__(self):
        if len(self.calls) >= self.max_calls:
            time.sleep(self.period - self._timespan)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.calls.append(time.time())
        while self._timespan >= self.period:
            self.calls.popleft()

    @property
    def _timespan(self):
        return self.calls[-1] - self.calls[0]


class FreqLimiter:
    """
    Copy from: https://github.com/Ice-Cirno/HoshinoBot/blob/master/hoshino/util/__init__.py
    """

    def __init__(self, default_cd_seconds):
        self.next_time = defaultdict(float)
        self.default_cd = default_cd_seconds

    def check(self, key) -> bool:
        return bool(time.time() >= self.next_time[key])

    def start_cd(self, key, cd_time=0):
        self.next_time[key] = time.time() + (
            cd_time if cd_time > 0 else self.default_cd
        )

    def left_time(self, key) -> float:
        return self.next_time[key] - time.time()


class DailyLimiter:
    """
    Copy from: https://github.com/Ice-Cirno/HoshinoBot/blob/master/hoshino/util/__init__.py
    """

    tz = pytz.timezone("Asia/Shanghai")

    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        now = datetime.now(self.tz)
        day = (now - timedelta(hours=6)).day
        if day != self.today:
            self.today = day
            self.count.clear()
        return bool(self.count[key] < self.max)

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, num=1):
        self.count[key] += num

    def reset(self, key):
        self.count[key] = 0
