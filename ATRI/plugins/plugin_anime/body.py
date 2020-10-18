#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   body.py
@Time    :   2020/10/11 14:38:23
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import json

from utils.utils_error import errorRepo
from utils.utils_request import request_get

class SauceNAO:

    def __init__(self, api_key, output_type=2, testmode=0, dbmask=None, dbmaski=32768, db=5, numres=1):
        api = 'https://saucenao.com/search.php'
        self.api = api
        params = dict()
        params['api_key'] = api_key
        params['output_type'] = output_type
        params['testmode'] = testmode
        params['dbmask'] = dbmask
        params['dbmaski'] = dbmaski
        params['db'] = db
        params['numres'] = numres
        self.params = params

    def search(self, url):
        self.params['url'] = url
        return request_get(self.api, self.params)

def resultRepo(user: str, key: str, img_url: str):
    try:
        task = SauceNAO(key)
        data = task.search(img_url)
    except Exception:
        return errorRepo('请求数据失败')

    data = json.loads(data)['results'][0]
    msg0 = ''
    print(data)

    msg0 += f'[CQ:at,qq={user}]\n'
    msg0 += f"SauceNAO INFO:\n"
    msg0 += f"[CQ:image,file={data['header'].get('thumbnail', None)}]\n"
    msg0 += f"Like：{data['header'].get('similarity', 0)}%\n"
    msg0 += f"Title：{data['data'].get('title', None)}\n"
    msg0 += f"Pixiv ID：{data['data'].get('pixiv_id', None)}\n"
    msg0 += f"Author：{data['data'].get('member_name', None)}\n"
    msg0 += f"Autoor ID：{data['data'].get('member_id', None)}\n"
    msg0 += f"Pixiv URL: https://www.pixiv.net/artworks/{data['data'].get('pixiv_id', None)}\n"
    msg0 += f"Pic URL: https://pixiv.cat/{data['data'].get('pixiv_id', None)}.jpg"

    if float(data['header'].get('similarity', 0)) < 65:
        msg0 += '注：相似率小于65%不一定正确'
    
    return msg0