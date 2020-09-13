import os
import requests
import base64
import nonebot
import time
from datetime import datetime
from random import choice
from pathlib import Path
from nonebot import on_command, CommandSession

import config
from ATRI.modules.error import errorBack
from ATRI.modules.funcControl import checkSwitch, checkNoob


bot = nonebot.get_bot()
master = config.SUPERUSERS
key = config.FaceplusAPI
secret = config.FaceplusSECRET
__plugin_name__ = "change_face"


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


#获取图片的人脸特征参数
def find_face(imgpath):
    url='https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {'api_key':key,'api_secret':secret,'image_url':imgpath,'return_landmark':1}
    files = {'image_file':open(imgpath,'rb')}
    response = requests.post(url,data=data,files=files)
    res_json = response.json()
    faces = res_json['faces'][0]['face_rectangle']    #获取面部大小的四个值，分别为长宽高低{'width': 176, 'top': 128, 'left': 80, 'height': 176}
    return faces


#换脸,函数传参中number表示两张脸的相似度为99%
def change_face(image_1, image_2, user, number=99):
    url = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    find_p1 = find_face(image_1)
    find_p2 = find_face(image_2)
    rectangle1 = str(str(find_p1['top'])+','+str(find_p1['left'])+','+str(find_p1['width'])+','+str(find_p1['height']))   #得到一个坐标
    rectangle2 = str(str(find_p2['top'])+','+str(find_p2['left'])+','+str(find_p2['width'])+','+str(find_p2['height']))
    
    page1 = open(image_1,'rb')      #以二进制打开图片1
    page1_64 = base64.b64encode(page1.read())    #将字符串转成成base64编码
    page1.close()

    page2 = open(image_2,'rb')
    page2_64 = base64.b64encode(page2.read())
    page2.close()

    data = {'api_key':key,'api_secret':secret,'template_base64':page1_64,
    'template_rectangle':rectangle1,'merge_base64':page2_64,'merge_rectangele':rectangle2,'merge_rate':number}
    response = requests.post(url,data=data).json()
    results = response['result']
    image = base64.b64decode(results)
    files = 'test'
    files = f'ATRI/data/temp/face/{user}'
    if not os.path.exists(files):
        os.mkdir(files)
    with open(files + '/img3.jpg','wb') as file:
        file.write(image)
    print('success!')


# change_face('1.jpg','2.jpg')


@on_command('ai_ch_face', aliases = ['AI换脸', 'ai换脸'], only_to_me = False)
async def AIchFace(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            await session.send(
                choice(
                    [
                        'zzzz......',
                        'zzzzzzzz......',
                        'zzz...好涩哦..zzz....',
                        '别...不要..zzz..那..zzz..',
                        '嘻嘻..zzz..呐~..zzzz..'
                    ]
                )
            )
        else:
            if checkSwitch(__plugin_name__, group):
                img1 = session.get('message1', prompt = '请发送需要换脸的图片')
                img2 = session.get('message2', prompt = '请发送素材图片')

                try:
                    # 我承认了，我是取名废！
                    a = img1.split(',')
                    a = a[2].replace(']', '')
                    a = a.replace('url=', '')
                    imgres1 = requests.get(a)

                    b = img2.split(',')
                    b = b[2].replace(']', '')
                    b = b.replace('url=', '')
                    imgres2 = requests.get(b)
                except:
                    session.finish(errorBack('获取图片失败'))

                try:
                    file1 = f'ATRI/data/temp/face/{user}'
                    if not os.path.exists(file1):
                        os.mkdir(file1)
                    with open(file1 + '/img1.jpg', 'wb') as f:
                        f.write(imgres1.content)

                    file2 = f'ATRI/data/temp/face/{user}'
                    if not os.path.exists(file2):
                        os.mkdir(file2)
                    with open(file2 + '/img2.jpg', 'wb') as f:
                        f.write(imgres2.content)
                except:
                    session.finish(errorBack('加载图片失败'))
                
                img1File = Path('.') / 'ATRI' / 'data' / 'temp' / 'face' / f'{user}' / 'img1.jpg'
                img2File = Path('.') / 'ATRI' / 'data' / 'temp' / 'face' / f'{user}' / 'img2.jpg'

                try:
                    change_face(img1File, img2File, user, 1)
                except:
                    session.finish(errorBack('换脸操作失败'))
                
                time.sleep(0.5)
                doneIMG = Path('.') / 'ATRI' / 'data' / 'temp' / 'face' / f'{user}' / 'img3.jpg'
                img = os.path.abspath(doneIMG)
                await session.send(f'[CQ:image,file=file:///{img}]')
                files = f'ATRI/data/temp/face/{user}'
                os.remove(files)
    
            else:
                session.finish('该功能已关闭...')

@AIchFace.args_parser
async def _(session: CommandSession):
    if not session.is_first_run and session.current_arg.startswith('算了'):
        session.switch(session.current_arg[len('算了'):])



# def f_1(x, A, B):
#     return A*x + B

# @on_command('change_u_head', aliases = ['接头霸王'], only_to_me = False)
# async def _(session: CommandSession):
#     user = session.event.user_id
#     with open("ATRI/plugins/switch/switch.json", 'r') as f:
#         data = json.load(f)
    
#     if data["change_face"] == 0:
#         with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
#             data0 = json.load(f)
        
#         if str(user) in data0.keys():
#             pass
#         else:
#             img1 = session.get('img1', prompt = '请发送需要换头的图片')
#             a = img1.split(',')
#             a = a[2].replace(']', '')
#             a = a.replace('url=', '')
#             print(a)
#             try:
#                 imgres1 = requests.get(a)
#                 file1 = f'ATRI/data/temp/head/{user}'
#                 if not os.path.exists(file1):
#                     os.mkdir(file1)
#                 with open(file1 + '/img1.jpg', 'wb') as f:
#                     f.write(imgres1.content)
#             except:
#                 session.finish('获取数据貌似失败了呢...')
#             img1File = Path('.') / 'ATRI' / 'data' / 'temp' / 'head' / f'{user}' / 'img1.jpg'

#             imgN = Path('.') / 'ATRI' / 'data' / 'img' / 'kyaru' / 'idk.png '
#             img = os.path.abspath(imgN)
#             await session.send(f'[CQ:image,file=:///{img}]')
#             head = session.get('head', prompt = '请输入头的序号，例如选择：1，发送：1')
#             if head.isdigit():
#                 pass
#             else:
#                 await session.send('请输入阿拉伯数字！')
#                 return
#             headIMG = Path('.') / 'ATRI' / 'data' / 'img' / 'kyaru' / f'{int(head)}.png'

#             try:
#                 img = cv2.imread(img1File)
#                 face_cascade = cv2.CascadeClassifier(cv2.haarcascades + r'haarcascade_frontalface_default.xml')
#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                 faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.15, minNeighbors = 5, minSize = (5, 5))
#                 await session.send(faces)

#             except:
#                 session.finish('emm...貌似焊接失败了呢......')
            
#             time.sleep(0.5)
#             doneIMG = Path('.') / 'ATRI' / 'data' / 'temp' / 'head' / f'{user}' / 'img3.jpg'
#             img = os.path.abspath(doneIMG)
#             await session.send(f'[CQ:image,file=file:///{img}]')
#             files = f'ATRI/data/temp/head/{user}'
#             os.remove(files)