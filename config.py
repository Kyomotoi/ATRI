import os
import json
import time
from nonebot.default_config import *

print("正在导入记忆模块ing...")
with open('config.json', 'r', encoding='UTF-8') as f:
    data = json.load(f)

# 如果您不是开发者不建议更改
DEBUG = False

# 加载监听的 IP 和 端口
HOST = data["HOST"]
PORT = data["PORT"]

# 机器人在繁忙之时的回复
SESSION_RUNNING_EXPRESSION = data["SESSION_RUNNING_EXPRESSION"]

# 机器人在用户取消操作时的回复
SESSION_CANCEL_EXPRESSION = data["SESSION_CANCEL_EXPRESSION"]

# 机器人的主人（QQ号）即 超级用户
try:
    SUPERUSERS = data["SUPERUSERS"]
    print("主人已识别！")
except:
    print("ATRI无法从记忆储蓄模块找到主人...如需帮助，请查看安装手册")
    time.sleep(1)
    print("仿生人没有主人是无法继续存在的！将于三秒后执行休眠...")
    time.sleep(3)
    os._exit(0)

# 机器人名称，替代 @ 和 命令开头
try:
    NICKNAME = data["NICKNAME"]
    print("对ATRI的特别称呼已加载！")
except:
    print("ATRI没特别的小昵称嘛...彳亍8")
    time.sleep(1)
    print("既然这样那叫我ATRI就好力！")
    NICKNAME = {'ATRI', 'アトリ'}
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

# 自定义命令开头
try:
    COMMAND_START = data["COMMAND_START"]
    print("呼叫指令已加载！")
except:
    print("如果没指定特别呼叫ATRI的手势的话，直接称呼我名称吧！")
    COMMAND_START = {'ATRI', ''}
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

# API url:https://api.lolicon.app/#/setu
try:
    LoliconAPI = data["API"]["LoliconAPI"]
    print("涩图大门的钥匙已到手！")
except:
    print("似乎没拿到大门的钥匙呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

# API url:https://www.faceplusplus.com.cn/
try:
    FaceplusAPI = data["API"]["FaceplusAPI"]
    print("用于人脸识别的钥匙已到手！")
except:
    print("貌似没拿到人脸识别的钥匙呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)
try:
    FaceplusSECRET = data["API"]["FaceplusSECRET"]
    print("用于人脸识别的验证码已到手！")
except:
    print("貌似没拿到人脸识别的验证码呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

# API url:https://cloud.baidu.com/
try:
    BaiduApiID = data["API"]["BaiduApiID"]
    print("用于图片识别的ID已到手！")
except:
    print("貌似没拿到图片识别的ID呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)
try:
    BaiduApiKEY = data["API"]["BaiduApiKEY"]
    print("用于图片识别的KEY已到手！")
except:
    print("貌似没拿到图片识别的KEY呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)
try:
    BaiduApiSECRET = data["API"]["BaiduApiSECRET"]
    print("用于图片识别的SECRET已到手！")
except:
    print("貌似没拿到图片识别的SECRET呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

# API url:https://saucenao.com/search.php
try:
    SauceNaoKEY = data["API"]["SauceNaoKEY"]
    print("用于SAUCENAO的钥匙已到手！")
except:
    print("貌似没拿到SAUCENAO的钥匙呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)