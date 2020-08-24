import os
import time
from nonebot.default_config import *

#配置监听的 IP 和 端口
HOST = '127.0.0.1'
PORT = 8080

# 机器人的主人（QQ号）即 超级用户
SUPERUSERS = [123456789]
def MASTER():
    return 123456789

# 机器人名称，替代 @ 和 命令开头
NICKNAME = {'ATRI', '亚托莉', 'アトリ'}

# 自定义命令开头
COMMAND_START = {''}

# API url:https://api.lolicon.app/#/setu
a = "" # key
def LOLICONAPI():
    return a

# API url:https://www.faceplusplus.com.cn/
b = ""
def FACE_KEY():
    return b

c = ""
def FACE_SECRET():
    return c

# API url:https://cloud.baidu.com/
def BAIDU_APP_ID():
    return 123 # id

d = "" # key
def BAIDU_API_KEY():
    return d

e = "" # secret
def BAIDU_SECRET():
    return e














#以下请勿删除

print("正在导入记忆模块ing...")

if SUPERUSERS:
    print("主人已识别！")
else:
    print("ATRI无法从记忆储蓄模块找到主人...如需帮助，请查看安装手册")
    time.sleep(1)
    print("仿生人没有主人是无法继续存在的！将于三秒后执行休眠...")
    time.sleep(3)
    os._exit(0)

if NICKNAME:
    print("对ATRI的特别称呼已加载！")
else:
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
    
if COMMAND_START:
    print("呼叫指令已加载！")
else:
    print("如果没指定特别呼叫ATRI的手势的话，直接称呼我名称吧！")
    COMMAND_START = {'ATRI', ''}
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

if LOLICONAPI():
    print("涩图大门的钥匙已到手！")
else:
    print("似乎没拿到大门的钥匙呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

if FACE_KEY():
    print("用于人脸识别的钥匙已到手！")
else:
    print("貌似没拿到人脸识别的钥匙呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

if FACE_SECRET():
    print("用于人脸识别的验证码已到手！")
else:
    print("貌似没拿到人脸识别的验证码呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

if BAIDU_APP_ID():
    print("用于图片识别的ID已到手！")
else:
    print("貌似没拿到图片识别的ID呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

if BAIDU_API_KEY():
    print("用于图片识别的KEY已到手！")
else:
    print("貌似没拿到图片识别的KEY呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or wait == 'y':
        pass
    else:
        os._exit(0)

if BAIDU_SECRET():
    print("用于图片识别的SECRET已到手！")
else:
    print("貌似没拿到图片识别的SECRET呢...如需帮助，请查看安装手册")
    print("...跳过！")
    time.sleep(1)
    wait = input("是否继续： Y/N\n")
    if wait == "Y" or 'y':
        pass
    else:
        os._exit(0)