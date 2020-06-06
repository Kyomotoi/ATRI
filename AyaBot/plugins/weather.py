import os
import re
import sys
sys.path.append('D:\code\Aya\AyaBot\plugins\Module')
import json
import requests
from nonebot import on_command, CommandSession
import google_translate

API_URL = 'https://api.weatherbit.io/v2.0/current?city={city}'
API_URL_2 = ',CN&key=1df2eb2951f3470a94cb323bb4647c18'


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


@on_command('weather', aliases=['查天气', '天气', '天气情况'], only_to_me=False)
async def weather(session: CommandSession):
    city = session.get('city', prompt='请键入你需要查询的城市(例:北京)')
    re_msg = google_translate.translate(city[:4999], to='en', source='zh-CN')
    URL = API_URL + re_msg[0] + API_URL_2
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

@on_command('wtlist', aliases=['天气详细'])
async def _(session: CommandSession):
    city = session.get('city', prompt='请键入你需要查询的城市(例:北京)')
    session.send('正在搜寻...')
    re_msg = google_translate.translate(city[:4999], to='en', source='zh-CN')
    URL = API_URL + re_msg[0] + API_URL_2
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



@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市不能为空，请重新输入')
    session.state[session.current_key] = stripped_arg