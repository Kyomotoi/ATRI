# -*- coding:utf-8 -*-
import time
import httpx
import string
import nonebot
import hashlib
from AyaBot.plugins import *
from random import randint
from urllib.parse import urlencode
from nonebot.helpers import context_id, render_expression
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand

bot = nonebot.get_bot()

ERROR_REPLY = (
    '吾辈不是很能理解主人的意思...',
    '(。´・ω・)ん?',
    'ん？',
    'あつ...脑子坏了..理解不能',
    '吾辈想听主人再说一次...'
)

class Chat(object):
    URL = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    app_id = bot.config.TX_APP_ID
    app_key = bot.config.TX_APPKEY
    print(app_id, app_key)
    nonce_str_example = 'fa577ce340859f9fe'
    ct = lambda: time.time()

    @classmethod
    def get_nonce_str(self):
        nonce_str = ''
        len_str = string.digits + string.ascii_letters
        for i in range(len(self.nonce_str_example)):
            nonce_str += len_str[randint(0, len(len_str) - 1)]
        return nonce_str

    @classmethod
    def sign(self, req_data):
        new_list = sorted(req_data.items())
        encode_list = urlencode(new_list)
        req_data = encode_list + "&" + "app_key" + "=" + self.app_key
        md5 = hashlib.md5()
        md5.update(req_data.encode('utf-8'))
        data = md5.hexdigest()
        return data.upper()

    @classmethod
    async def request(self, text):
        req_data = {
            'app_id': self.app_id,
            'time_stamp': int(self.ct()),
            'nonce_str': self.get_nonce_str(),
            'session': 10000,
            'question': text,
        }
        print(req_data)
        req_data['sign'] = self.sign(req_data)
        req_data = sorted(req_data.items())
        requests = httpx.AsyncClient()
        result = await requests.get(self.URL, params=req_data)
        await requests.aclose()
        result = result.json()
        print(result)
        if result['ret'] == 0:
            return result['data']['answer']
        return render_expression(ERROR_REPLY)


@on_command('chat')
async def chat(session: CommandSession):
    msg = session.state.get('msg')
    reply = await Chat.request(msg)
    await session.finish(reply)
    return

@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, ('chat'), {'msg': session.msg_text})