import time
import pytz
from datetime import datetime


def get_date():
    tz = pytz.timezone('Asia/Shanghai')
    t = datetime.fromtimestamp(int(time.time()),
        pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')

def get_year():
    tz = pytz.timezone('Asia/Shanghai')
    t = datetime.fromtimestamp(int(time.time()),
        pytz.timezone('Asia/Shanghai')).strftime('%Y')

def get_month():
    tz = pytz.timezone('Asia/Shanghai')
    t = datetime.fromtimestamp(int(time.time()),
        pytz.timezone('Asia/Shanghai')).strftime('%m')

def get_day():
    tz = pytz.timezone('Asia/Shanghai')
    t = datetime.fromtimestamp(int(time.time()),
        pytz.timezone('Asia/Shanghai')).strftime('%d') 