import requests
import nonebot
import re
from nonebot import on_command, CommandSession, CQHttpError


@on_command('fan', aliases=['搜番', '查番', '番剧搜索', '搜索番剧'], only_to_me=False)
async def seach_fan(session: CommandSession):
    year = session.get('year', prompt='你想查找哪一年的番呢?(示范:2020)')
    month = session.get('month', prompt='你想查找哪个月的番呢(示范:4)?')
    await session.send('查询的情况如下:')
    await session.send('日期:' + year + month)
    # await session.send('标题:' + title)
    # await session.send('链接:' + link)


@seach_fan.args_parser
async def _(session: CommandSession):
    # if session.is_first_run:
    #     return
    if session.current_key == 'year':
        if not re.fullmatch(r'\d{4}', session.current_arg_text):
            session.pause('日期格式有误，请重新输入(示范:2020)')
    
    if session.current_key == 'month':
        if not re.fullmatch(r'\d{2}', session.current_arg_text):
            session.pause('日期格式有误，请重新输入(示范:4)')


    # try:
    # except CQHttpError:
    #     await session.send('请求未响应或出错，请重试')

