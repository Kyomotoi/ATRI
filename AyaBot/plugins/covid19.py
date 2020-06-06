import re
import json
import demjson
import requests
from pprint import pformat, pprint
from urllib.parse import urlencode
from nonebot import on_command, CommandSession


# 国外版 数据更新非常及时
# 必须挂木弟子
# 成功把之前的屎优化了！OHHHHHHHHHHHH
# 如需使用国内版，请查看下面的链接，下载后与这个文件替换
# https://github.com/Kyomotoi/covid19/tree/master/Domestic



url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"


LIST = """截至: {lastChecked}
国家: {location}
已治愈: {recovered}
已经死亡: {deaths}
总感染数: {confirmed}
现存感染人数: {nowConfirmed}
最后检查时间: {lastReported}"""


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


@on_command('covid19', aliases=['疫情', '疫情查询', '疫情情况'], only_to_me=False)
async def covid19(session: CommandSession):
    country = session.get('country', prompt='请用Eng键入需要查询的国家(例:China)')
    re_msg = translate(country[:4999], to='en', source='zh-CN')
    # if re_msg[0]!='':
    #     await session.send(re_msg[0])
    await session.send('开始搜寻...\n如返回国名为Global的则为提供的国家名有问题，必须为英文全称')
    try:
        querystring = {"country":"cy"}
        querystring["country"] = re_msg[0]
        print(querystring)
        headers = {
            'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
            'x-rapidapi-key': "a852be0d03msh8bd4299fe71bfeep100861jsn185ea925449c"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        html = response.text
        c19 = json.loads(html)
        await session.send(LIST.format(
            lastChecked=c19["data"]["lastReported"],
            location=c19["data"]["location"],
            recovered=c19["data"]["recovered"],
            deaths=c19["data"]["deaths"],
            confirmed=c19["data"]["confirmed"],
            nowConfirmed=c19["data"]["confirmed"] - c19["data"]["deaths"] - c19["data"]["recovered"],
            lastReported=c19["data"]["lastChecked"],
            )
        )
    except:
        await session.send('搜索出问题了呢，重新试试?')