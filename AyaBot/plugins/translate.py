import re
import requests
import demjson
from pprint import pformat, pprint
from urllib.parse import urlencode
from nonebot import on_command, CommandSession

#FROM Joenothing-lst


def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint: 
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1 
    return val

def ansii(a):
    return a.encode('gbk')

def kr(a:int, b):
    c = 0
    b = ansii(b)
    while c < len(b)-2:
        d = b[c + 2]
        d = d - 87 if ansii("a")[0] <= d else int(chr(d))
        d = a >> d if ansii("+")[0] == b[c + 1] else a << d
        d = int_overflow(d)
        a = a + d & 4294967295 if ansii("+")[0] == b[c] else a ^ d
        c += 3
    return int_overflow(a)

def mr(q, TKK):
    e = q.encode()
    d = str(TKK).split('.')
    a = int(d[0])
    b = int(d[0])

    for f in e:
        a += f
        a = kr(a, "+-a^+6")
    a = kr(a, "+-3^+b+-f")
    a &= 0xffffffff # 出错了，转回无符号
    a ^= (int(d[1]) or 0)
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    a = int(a)

    # c = '&tk='
    # return c + (str(a) + "." + str(a ^ b))
    return (str(a) + "." + str(a ^ b))


"""
def Sr(a, TKK):
    a = ''.join(a['a']['b']['q'])
    return mr(a, TKK)
d = {
    'a':{
        'a': ['q'],
        'b': {
            'q': ['me']
        },
        'c': 1,
        'g': 1
    },
    'b': 1,
    'c': None,
    'j': False,
}
TKK = '426151.3141811846'
tk = Sr(d, TKK)
print(tk)
"""


session = requests.session()


def translate(q='hello', source='en', to='zh-CN', tkk=None):
    """
    限制最大5000,按utf-8算，一个汉字算1个,1个英文算一个，超过会失败
    """
    if not tkk:
        tkk = '426151.3141811846'
    tk = mr(q, tkk)
    params = {
        'client': 't',
        'sl': source,
        'tl': to,
        'hl': source,
        'dt': [
            'at', 'qca', 'rw', 'rm', 'ss', 't'
            ],
        'tk': tk,
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'pc': 1,
        'kc': 1,
        'ssel': 0,
        'otf': 1
    }
    data = {
        'q': q
    }
    headers = {
        'Referer': 'https://translate.google.cn/',
        'Host': 'translate.google.cn',
    }
    resp = requests.post('https://translate.google.cn/translate_a/single', params=params, data=data, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        data = resp.json()
        
        result = []
        result.append(''.join(map(lambda x:x[0], data[0][:-1])))
        result.append(data[0][-1][-1])
        return result
    else:
        return None


def ref_words(q='hello', source='en', to='zh-CN'):
    params = {
        'q': q,
        'client': 'translate-web',
        'ds': 'translate',
        'hl': source,
        'requiredfields': f'tl:{to}',
        'callback':'window.google.ref_words'
    }
    url = 'https://clients1.google.com/complete/search?'
    headers = {
        'Referer': 'https://translate.google.cn/',
        'Host': 'clients1.google.cn',
    }
    resp = session.get(url, params=params, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        result = re.search(r'window.google.ref_words\((.*)\)', resp.text).group(1)
        json_data = demjson.decode(result)
        data_list = list(map(lambda x:x[0], json_data[1]))
        return data_list
    else:
        return None


@on_command('ja_to_zh', aliases=('日语翻译',), only_to_me=False)                 
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='zh-CN', source='ja')
        if re_msg[0]!='' and re_msg[0]!=msg:
            await session.send(re_msg[0])

@on_command('ja_to_en', aliases=('英语翻译',), only_to_me=False)                 
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='zh-CN', source='en')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_ja', aliases=('翻译日语',), only_to_me=False)
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='ja', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_en', aliases=('翻译英语',), only_to_me=False)
async def _(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='en', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])