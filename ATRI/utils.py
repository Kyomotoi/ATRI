import os
import yaml
from datetime import datetime
from pathlib import Path
from PIL import ImageFile
import PIL.Image as Image

from .exceptions import InvalidWriteText


def load_yaml(file: Path) -> dict:
    '''
    读取yaml文件
    :return: dict
    '''
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


def count_list(lst: list, aim) -> int:
    '''
    检查某列表中目标出现的次数
    :return: int
    '''
    count = 0
    for ele in lst:
        if ele == aim:
            count = count + 1
    return count


def del_list_aim(lst: list, aim) -> list:
    '''
    删除某列表中所有目标元素
    :return: list
    '''
    while aim in lst:
        lst.remove(aim)
    return lst


def now_time() -> float:
    '''
    获取当前时间（小时）
    :return: float
    '''
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now

def compress_image(out_file: str, kb=500, quality=85, k=0.9) -> str:
    '''
    压缩图片
    :return: img file
    '''
    o_size = os.path.getsize(out_file) // 1024
    if o_size <= kb:
        return out_file
    
    ImageFile.LOAD_TRUNCATED_IMAGES = True # type: ignore
    while o_size > kb:
        img = Image.open(out_file)
        x, y = img.size
        out = img.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:
            out.save(out_file, quality=quality)
        except InvalidWriteText:
            raise InvalidWriteText('Writing file failed!')
            break
        o_size = os.path.getsize(out_file) // 1024
    return out_file
