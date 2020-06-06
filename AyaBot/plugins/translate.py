# -*- coding:utf-8 -*-
import re
import sys
sys.path.append('D:\code\Aya\AyaBot\plugins\Module')
import demjson
import requests
from pprint import pformat, pprint
from urllib.parse import urlencode
from nonebot import on_command, CommandSession
import google_translate

#FROM Joenothing-lst


@on_command('ja_to_zh', aliases=('日语翻译',), only_to_me=False)                 
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = google_translate.translate(msg[:4999], to='zh-CN', source='ja')
        if re_msg[0]!='' and re_msg[0]!=msg:
            await session.send(re_msg[0])

@on_command('ja_to_en', aliases=('英语翻译',), only_to_me=False)                 
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = google_translate.translate(msg[:4999], to='zh-CN', source='en')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_ja', aliases=('翻译日语',), only_to_me=False)
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = google_translate.translate(msg[:4999], to='ja', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_en', aliases=('翻译英语',), only_to_me=False)
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = google_translate.translate(msg[:4999], to='en', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])