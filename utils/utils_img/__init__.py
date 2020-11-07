#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:40:17
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import os
import string
import aiohttp
import PIL.Image as Image
from pathlib import Path
from random import sample

from PIL import Image
from PIL import ImageFile

async def aio_download_pics(url) -> str:
    '''
    下载图片并重命名

    :return: img file
    '''
    path = Path('.') / 'ATRI' / 'data' / 'data_Temp' / 'img'
    path = os.path.abspath(path)
    img_key = ''.join(sample(string.ascii_letters + string.digits, 16))
    img = path + f'\\{img_key}.png'
    async with aiohttp.ClientSession() as session:         
        async with session.get(url) as response:                
            pic = await response.read()    #以Bytes方式读入非文字                     
            with open(img, mode='wb') as f:# 写入文件
                f.write(pic)
                f.close()
    return img

def compress_image(outfile: str, kb=400, quality=85, k=0.9) -> str:
    '''
    压缩图片

    :return: img file
    '''
    o_size = os.path.getsize(outfile) // 1024
    if o_size <= kb:
        return outfile
   
    ImageFile.LOAD_TRUNCATED_IMAGES = True # type: ignore
    while o_size > kb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
        try:
            out.save(outfile, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile
