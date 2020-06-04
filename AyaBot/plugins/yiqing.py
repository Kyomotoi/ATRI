import json
import requests
from datetime import datetime
from nonebot import on_command, CommandSession



# 屎 一 般 的 码
# 带 佬 看 了 别 骂 5 5 5
# 实 现 方 法 纯 调 用 字 典
# 等👴学有所成再回来改这坨屎



#获取当日国内各省市实时数据
url_1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
response_1 = requests.get(url=url_1).json()
data_1 = json.loads(response_1['data'])

# #获取历史数据/每日新增数据
# url_2 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
# response_2 = requests.get(url=url_2).json()
# data_2 = json.loads(response_2['data'])

#获取全球实时/历史数据，输入中国病例
url_3 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
response_3 = requests.get(url=url_3).json()
data_3 = json.loads(response_3['data'])

lastUpdateTime = data_1["lastUpdateTime"]
directory = "AyaBot\plugins\datayiqing\ "

filename1 = directory + lastUpdateTime.split(' ')[0] + "_data_1.json"
with open(filename1, "w", encoding="utf-8") as f:
    f.write(response_1['data'])
    f.close()

# filename2 = directory + lastUpdateTime.split(' ')[0] + "_data_2.json"
# with open(filename2, "w", encoding="utf-8") as f:
#     f.write(response_2['data'])
#     f.close()

filename3 = directory + lastUpdateTime.split(' ')[0] + "_data_3.json"
with open(filename3, "w", encoding="utf-8") as f:
    f.write(response_3['data'])
    f.close()



LIST_CN = """——————————————————
截至:{time}
国家:{name_cr}
总确诊病例:{confirm}
现存病例:{nowconfirm}
总疑似病例:{suspect}
总死亡病例:{dead}
总治愈病例:{heal}
——————————————————
今日确诊病例:{today_confirm}
"""

LIST_FG = """国外数据来源于世卫，故更新会略慢
——————————————————
日期:{date}
国家:{name_cr}
地理位置:{continent}
总确诊病例:{confirm}
现存病例:{nowconfirm}
总疑似病例:{suspect}
总死亡病例:{dead}
总治愈病例:{heal}
——————————————————
今日确诊病例:{today_confirm}
"""


@on_command('yiqing', aliases=['疫情', '疫情情况'], only_to_me=False)
async def yiqing(session: CommandSession):
    country = session.get('country', prompt='你想查哪个国家呢？(例:中国)')
    try:
        if country == "中国":
            f = open(filename1, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_CN.format(
                time=setting["lastUpdateTime"],
                name_cr=setting["areaTree"][0]["name"],
                confirm=setting["areaTree"][0]["total"]["confirm"],
                nowconfirm=setting["areaTree"][0]["total"]["nowConfirm"],
                suspect=setting["areaTree"][0]["total"]["suspect"],
                dead=setting["areaTree"][0]["total"]["dead"],
                heal=setting["areaTree"][0]["total"]["heal"],
                today_confirm=setting["areaTree"][0]["today"]["confirm"]
                )
            )
            
        elif country == "美国" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][0]["date"],
                name_cr=setting["foreignList"][0]["name"],
                continent=setting["foreignList"][0]["continent"],
                confirm=setting["foreignList"][0]["confirm"],
                nowconfirm=setting["foreignList"][0]["nowConfirm"],
                suspect=setting["foreignList"][0]["suspect"],
                dead=setting["foreignList"][0]["dead"],
                heal=setting["foreignList"][0]["heal"],
                today_confirm=setting["foreignList"][0]["confirmAdd"],
                )
            )
        
        elif country == "西班牙" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][1]["date"],
                name_cr=setting["foreignList"][1]["name"],
                continent=setting["foreignList"][1]["continent"],
                confirm=setting["foreignList"][1]["confirm"],
                nowconfirm=setting["foreignList"][1]["nowConfirm"],
                suspect=setting["foreignList"][1]["suspect"],
                dead=setting["foreignList"][1]["dead"],
                heal=setting["foreignList"][1]["heal"],
                today_confirm=setting["foreignList"][1]["confirmAdd"],
                )
            )
        
        elif country == "英国" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][2]["date"],
                name_cr=setting["foreignList"][2]["name"],
                continent=setting["foreignList"][2]["continent"],
                confirm=setting["foreignList"][2]["confirm"],
                nowconfirm=setting["foreignList"][2]["nowConfirm"],
                suspect=setting["foreignList"][2]["suspect"],
                dead=setting["foreignList"][2]["dead"],
                heal=setting["foreignList"][2]["heal"],
                today_confirm=setting["foreignList"][2]["confirmAdd"],
                )
            )
        
        elif country == "意大利" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][3]["date"],
                name_cr=setting["foreignList"][3]["name"],
                continent=setting["foreignList"][3]["continent"],
                confirm=setting["foreignList"][3]["confirm"],
                nowconfirm=setting["foreignList"][3]["nowConfirm"],
                suspect=setting["foreignList"][3]["suspect"],
                dead=setting["foreignList"][3]["dead"],
                heal=setting["foreignList"][3]["heal"],
                today_confirm=setting["foreignList"][3]["confirmAdd"],
                )
            )
        
        elif country == "德国" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][4]["date"],
                name_cr=setting["foreignList"][4]["name"],
                continent=setting["foreignList"][4]["continent"],
                confirm=setting["foreignList"][4]["confirm"],
                nowconfirm=setting["foreignList"][4]["nowConfirm"],
                suspect=setting["foreignList"][4]["suspect"],
                dead=setting["foreignList"][4]["dead"],
                heal=setting["foreignList"][4]["heal"],
                today_confirm=setting["foreignList"][4]["confirmAdd"],
                )
            )
        
        elif country == "伊朗" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][5]["date"],
                name_cr=setting["foreignList"][5]["name"],
                continent=setting["foreignList"][5]["continent"],
                confirm=setting["foreignList"][5]["confirm"],
                nowconfirm=setting["foreignList"][5]["nowConfirm"],
                suspect=setting["foreignList"][5]["suspect"],
                dead=setting["foreignList"][5]["dead"],
                heal=setting["foreignList"][5]["heal"],
                today_confirm=setting["foreignList"][5]["confirmAdd"],
                )
            )
        
        elif country == "加拿大" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][6]["date"],
                name_cr=setting["foreignList"][6]["name"],
                continent=setting["foreignList"][6]["continent"],
                confirm=setting["foreignList"][6]["confirm"],
                nowconfirm=setting["foreignList"][6]["nowConfirm"],
                suspect=setting["foreignList"][6]["suspect"],
                dead=setting["foreignList"][6]["dead"],
                heal=setting["foreignList"][6]["heal"],
                today_confirm=setting["foreignList"][6]["confirmAdd"],
                )
            )
        
        elif country == "法国" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][7]["date"],
                name_cr=setting["foreignList"][7]["name"],
                continent=setting["foreignList"][7]["continent"],
                confirm=setting["foreignList"][7]["confirm"],
                nowconfirm=setting["foreignList"][7]["nowConfirm"],
                suspect=setting["foreignList"][7]["suspect"],
                dead=setting["foreignList"][7]["dead"],
                heal=setting["foreignList"][7]["heal"],
                today_confirm=setting["foreignList"][7]["confirmAdd"],
                )
            )
        
        elif country == "瑞士" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][8]["date"],
                name_cr=setting["foreignList"][8]["name"],
                continent=setting["foreignList"][8]["continent"],
                confirm=setting["foreignList"][8]["confirm"],
                nowconfirm=setting["foreignList"][8]["nowConfirm"],
                suspect=setting["foreignList"][8]["suspect"],
                dead=setting["foreignList"][8]["dead"],
                heal=setting["foreignList"][8]["heal"],
                today_confirm=setting["foreignList"][8]["confirmAdd"],
                )
            )
        
        elif country == "奥地利" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][9]["date"],
                name_cr=setting["foreignList"][9]["name"],
                continent=setting["foreignList"][9]["continent"],
                confirm=setting["foreignList"][9]["confirm"],
                nowconfirm=setting["foreignList"][9]["nowConfirm"],
                suspect=setting["foreignList"][9]["suspect"],
                dead=setting["foreignList"][9]["dead"],
                heal=setting["foreignList"][9]["heal"],
                today_confirm=setting["foreignList"][9]["confirmAdd"],
                )
            )
        
        elif country == "比利时" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][10]["date"],
                name_cr=setting["foreignList"][10]["name"],
                continent=setting["foreignList"][10]["continent"],
                confirm=setting["foreignList"][10]["confirm"],
                nowconfirm=setting["foreignList"][10]["nowConfirm"],
                suspect=setting["foreignList"][10]["suspect"],
                dead=setting["foreignList"][10]["dead"],
                heal=setting["foreignList"][10]["heal"],
                today_confirm=setting["foreignList"][10]["confirmAdd"],
                )
            )
        
        elif country == "荷兰" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][11]["date"],
                name_cr=setting["foreignList"][11]["name"],
                continent=setting["foreignList"][11]["continent"],
                confirm=setting["foreignList"][11]["confirm"],
                nowconfirm=setting["foreignList"][11]["nowConfirm"],
                suspect=setting["foreignList"][11]["suspect"],
                dead=setting["foreignList"][11]["dead"],
                heal=setting["foreignList"][11]["heal"],
                today_confirm=setting["foreignList"][11]["confirmAdd"],
                )
            )
        
        elif country == "韩国" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][12]["date"],
                name_cr=setting["foreignList"][12]["name"],
                continent=setting["foreignList"][12]["continent"],
                confirm=setting["foreignList"][12]["confirm"],
                nowconfirm=setting["foreignList"][12]["nowConfirm"],
                suspect=setting["foreignList"][12]["suspect"],
                dead=setting["foreignList"][12]["dead"],
                heal=setting["foreignList"][12]["heal"],
                today_confirm=setting["foreignList"][12]["confirmAdd"],
                )
            )
        
        elif country == "土耳其" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][13]["date"],
                name_cr=setting["foreignList"][13]["name"],
                continent=setting["foreignList"][13]["continent"],
                confirm=setting["foreignList"][13]["confirm"],
                nowconfirm=setting["foreignList"][13]["nowConfirm"],
                suspect=setting["foreignList"][13]["suspect"],
                dead=setting["foreignList"][13]["dead"],
                heal=setting["foreignList"][13]["heal"],
                today_confirm=setting["foreignList"][13]["confirmAdd"],
                )
            )
        
        elif country == "塞尔维亚" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][14]["date"],
                name_cr=setting["foreignList"][14]["name"],
                continent=setting["foreignList"][14]["continent"],
                confirm=setting["foreignList"][14]["confirm"],
                nowconfirm=setting["foreignList"][14]["nowConfirm"],
                suspect=setting["foreignList"][14]["suspect"],
                dead=setting["foreignList"][14]["dead"],
                heal=setting["foreignList"][14]["heal"],
                today_confirm=setting["foreignList"][14]["confirmAdd"],
                )
            )
        
        elif country == "葡萄牙" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][15]["date"],
                name_cr=setting["foreignList"][15]["name"],
                continent=setting["foreignList"][15]["continent"],
                confirm=setting["foreignList"][15]["confirm"],
                nowconfirm=setting["foreignList"][15]["nowConfirm"],
                suspect=setting["foreignList"][15]["suspect"],
                dead=setting["foreignList"][15]["dead"],
                heal=setting["foreignList"][15]["heal"],
                today_confirm=setting["foreignList"][15]["confirmAdd"],
                )
            )
        
        elif country == "俄罗斯" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][30]["date"],
                name_cr=setting["foreignList"][30]["name"],
                continent=setting["foreignList"][30]["continent"],
                confirm=setting["foreignList"][30]["confirm"],
                nowconfirm=setting["foreignList"][30]["nowConfirm"],
                suspect=setting["foreignList"][30]["suspect"],
                dead=setting["foreignList"][30]["dead"],
                heal=setting["foreignList"][30]["heal"],
                today_confirm=setting["foreignList"][30]["confirmAdd"],
                )
            )

        elif country == "日本" :
            f = open(filename3, encoding='utf-8')
            setting = json.load(f)
            await session.send(LIST_FG.format(
                date=setting["foreignList"][31]["date"],
                name_cr=setting["foreignList"][31]["name"],
                continent=setting["foreignList"][31]["continent"],
                confirm=setting["foreignList"][31]["confirm"],
                nowconfirm=setting["foreignList"][31]["nowConfirm"],
                suspect=setting["foreignList"][31]["suspect"],
                dead=setting["foreignList"][31]["dead"],
                heal=setting["foreignList"][31]["heal"],
                today_confirm=setting["foreignList"][31]["confirmAdd"],
                )
            )
    except:
        await session.send('获取数据时出问题，请重试')
        return









