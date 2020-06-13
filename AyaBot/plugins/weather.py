# -*- coding:utf-8 -*-
import os
import re
import sys
sys.path.append(r'请改成你机器人的对应目录\Aya\AyaBot\plugins\Module')
import json
import requests
from nonebot import on_command, CommandSession
import google_translate

API_URL = 'https://api.weatherbit.io/v2.0/current?city='
API_URL_2 = '&key=1df2eb2951f3470a94cb323bb4647c18'
API_URL_3 = 'https://www.tianqiapi.com/free/day?appid=36628957&appsecret=WKn4dtVg&city='


LIST = """{city} 情况如下:
截至: {ob_time}
天气: {description}
温度: {temp}
风速: {wind_spd}
风向: {wind_cdir}
云覆盖率(%): {clouds}"""

LIST_ALL = """{city} 详细情况如下:
纬度(°): {lat}
经度(°): {lon}
日出时间(HH:MM): {sunrise}
日落时间(HH:MM): {sunset}
本地时区: {timezone}
源站ID: {station}
上次观察时间(YYYY-MM-DD HH:MM): {ob_time}
当前周期小时(YYYY-MM-DD HH:MM): {datetime}
压力(mb): {pres}
海平面压力(mb): {slp}
风速(m/s): {wind_spd}
风向(°): {wind_dir}
缩写风向: {wind_cdir}
风向全称: {wind_cdir_full}
温度(℃): {temp}
感觉温度(℃): {app_temp}
相对湿度(%): {rh}
露点(℃): {dewpt}
云覆盖率(%): {clouds}
一天的一部分(d/n): {pod}
现在天气: {description}
可见度(km): {vis}
液体当量沉淀速率(mm/hr): {precip}
降雪(mm/h): {snow}
紫外线指数(0-11+): {uv}
空气质量指数[美国-EPA标准0-+500] [Clear Sky]: {aqi}
漫射水平太阳辐照度(W/m^2) [Clear Sky]: {dhi}
普通太阳直射辐射(W/m^2) [Clear Sky]: {dni}
全球水平太阳辐照度(W/m^2): {ghi}
估计的太阳辐射(W/m^2): {solar_rad}
太阳斜角(°): {elev_angle}
太阳时角(°): {h_angle}"""

LIST_CN = """{city} 今日信息如下:
更新时间:{time}
天气情况:{wea}
空气质量:{air}
温度:
    现在温度:{tem}
    最高温度:{temday}
    最低温度:{temnight}
风向:{win}
风力等级:{winspeed}
风速:{winmeter}"""


@on_command('weather', aliases=['天气'], only_to_me=False)
async def weather(session: CommandSession):
    cy_ct = session.get('weather', prompt='输入的信息似乎出问题了呢...例:天气 CN 北京 或 天气 JP 东京')
    ms = cy_ct.split(' ')
    try:
        country = ms[0]
        city = ms[1]
        re_msg = google_translate.translate(city[:4999], to='en', source='zh-CN')
        URL = API_URL + re_msg[0] + ',' + country + API_URL_2
        # print(URL)
        res = requests.get(URL)
        res.encoding = 'utf-8'
        html = res.text
        wt = json.loads(html)
        await session.send(LIST.format(
            city=wt["data"][0]["city_name"],
            ob_time=wt["data"][0]["ob_time"],
            description=wt["data"][0]["weather"]["description"],
            temp=wt["data"][0]["temp"],
            wind_spd=wt["data"][0]["wind_spd"],
            wind_cdir=wt["data"][0]["wind_cdir"],
            clouds=wt["data"][0]["clouds"],
            )
        )
    except:
        await session.send('搜索似乎出问题了呢...请重试')

@on_command('wtlist', aliases=['天气详细'])
async def wtlist(session: CommandSession):
    cy_ct = session.get('wtlist', prompt='输入的信息似乎出问题了呢...例:天气 CN 北京 或 天气 JP 东京')
    ms = cy_ct.split(' ')
    try:
        country = ms[0]
        city = ms[1]
        re_msg = google_translate.translate(city[:4999], to='en', source='zh-CN')
        URL = API_URL + re_msg[0] + ',' + country + API_URL_2
        # print(URL)
        res = requests.get(URL)
        res.encoding = 'utf-8'
        html = res.text
        wt = json.loads(html)
        await session.send(LIST_ALL.format(
            rh=wt["data"][0]["rh"],
            pod=wt["data"][0]["pod"],
            lon=wt["data"][0]["lon"],
            pres=wt["data"][0]["pres"],
            timezone=wt["data"][0]["timezone"],
            ob_time=wt["data"][0]["ob_time"],
            clouds=wt["data"][0]["clouds"],
            solar_rad=wt["data"][0]["solar_rad"],
            city=wt["data"][0]["city_name"],
            wind_spd=wt["data"][0]["wind_spd"],
            last_ob_time=wt["data"][0]["last_ob_time"],
            wind_cdir_full=wt["data"][0]["wind_cdir_full"],
            wind_cdir=wt["data"][0]["wind_cdir"],
            temp=wt["data"][0]["temp"],
            slp=wt["data"][0]["slp"],
            vis=wt["data"][0]["vis"],
            h_angle=wt["data"][0]["h_angle"],
            sunset=wt["data"][0]["sunset"],
            dni=wt["data"][0]["dni"],
            dewpt=wt["data"][0]["dewpt"],
            snow=wt["data"][0]["snow"],
            uv=wt["data"][0]["uv"],
            precip=wt["data"][0]["precip"],
            wind_dir=wt["data"][0]["wind_dir"],
            sunrise=wt["data"][0]["sunrise"],
            ghi=wt["data"][0]["ghi"],
            dhi=wt["data"][0]["dhi"],
            aqi=wt["data"][0]["aqi"],
            lat=wt["data"][0]["lat"],
            description=wt["data"][0]["weather"]["description"],
            datetime=wt["data"][0]["datetime"],
            station=wt["data"][0]["station"],
            elev_angle=wt["data"][0]["elev_angle"],
            app_temp=wt["data"][0]["app_temp"],
            )
        )
    except:
        await session.send('搜索似乎出问题了呢...请重试')


@on_command('weathercn', aliases=['国内天气详细'], only_to_me=False)
async def weathercn(session: CommandSession):
    city = session.get('weathercn', prompt='输入格式似乎有问题呢...例:国内天气详细 北京')
    ms = city.split(' ')
    try:
        msg = ms[0]
        print(msg)
        res = API_URL_3 + msg
        print(res)
        res1 = requests.get(res)
        res1.encoding = 'utf-8'
        html = res1.text
        wt = json.loads(html)
        await session.send(LIST_CN.format(
            city=wt["city"],
            time=wt["update_time"],
            wea=wt["wea"],
            tem=wt["tem"],
            temday=wt["tem_day"],
            temnight=wt["tem_night"],
            win=wt["win"],
            winspeed=wt["win_speed"],
            winmeter=wt["win_meter"],
            air=wt["air"]
            )
        )
    except:
        await session.send('获取数据时出问题，请尝试发送:天气')
        return



@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['weather'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市不能为空，请重新输入')
    session.state[session.current_key] = stripped_arg

@wtlist.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['wtlist'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市不能为空，请重新输入')
    session.state[session.current_key] = stripped_arg

@weathercn.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['weathercn'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市不能为空，请重新输入')
    session.state[session.current_key] = stripped_arg
