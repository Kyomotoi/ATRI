# -*- coding:utf-8 -*-
from nonebot.default_config import *

#配置监听的 IP 和端口
HOST = '127.0.0.1'
PORT = 8080

#咱的主人(QQ号)
SUPERUSERS = {}

#机器人赋名，替代@
NICKNAME = {}

#自定义命令开头
COMMAND_START = {}

#推送屏蔽群名单
bangroup = []

#LOLICONAPI url:https://api.lolicon.app/#/setu
LOLICONAPI = ""

#腾讯ai url:https://ai.qq.com/
TX_APP_ID = ""
TX_APPKEY = ""
















#判定 请勿更改！
print("正在导入吾辈最最最重要的记忆......")
if SUPERUSERS:
    print("吾辈的主人已加载！")
else:
    print("吾辈没找到主人...如需帮助，请查看安装手册")

if NICKNAME:
    print("吾辈的称呼已加载！")
else:
    print("吾辈忘记自己叫啥惹...如需帮助，请查看安装手册")

if COMMAND_START:
    print("呼叫吾辈的特别小工具已加载！")
else:
    print("吾辈无法找到呼唤咱的特别小工具...如需帮助，请查看安装手册")

if bangroup:
    print("屏蔽群发的群已加载！")
else:
    print("主人似乎没给咱指定不需要接受群发的群号呢...那吾辈就可以更全面地进行推送了w")

if LOLICONAPI:
    print("涩图key已加载！")
else:
    print("吾辈似乎没给咱打开涩图大门的钥匙呢...如需帮助，请查看安装手册")

if TX_APP_ID:
    print("吾辈的腾讯识别码已加载！")
else:
    print("吾辈没法找到自己的腾讯识别码呢...如需帮助，请查看安装手册")

if TX_APPKEY:
    print("吾辈的腾讯key已加载！")
else:
    print("主人似乎没给咱腾讯key呢...如需帮助，请查看安装手册")