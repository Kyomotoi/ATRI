import json
import string
from pathlib import Path
from random import sample
from traceback import format_exc
from datetime import datetime
from typing import Optional


def errorBack(Lmsg: Optional[str] = None):
    try:
        with open(Path('.') / 'ATRI' / 'data' / 'errorData' / 'errorData.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    ran_str = ''.join(sample(string.ascii_letters + string.digits, 8))
    msg0 = f"{datetime.now()}\n"
    msg0 += f"{format_exc()}"
    data[f"{ran_str}"] = f"{msg0}"

    with open(Path('.') / 'ATRI' / 'data' / 'errorData' / 'errorData.json', 'w') as f:
        f.write(json.dumps(data))
        f.close()

    if Lmsg:
        pass
    else:
        Lmsg = 'unknown'

    msg0 = f'ERROR! Reason: [{Lmsg}]\n'
    msg0 += f'trackID: {ran_str}\n'
    msg0 += "请使用[来杯红茶]功能以联系维护者\n"
    msg0 += "并附上 trackID"

    return msg0