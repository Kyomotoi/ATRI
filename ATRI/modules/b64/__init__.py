import os
import time
import base64
import requests
from pathlib import Path
from PIL import Image, ImageGrab


path_emoji = Path('.') / 'ATRI' / 'data' / 'emoji'
path_temp_img = Path('.') / 'ATRI' / 'data' / 'temp' / 'img'
path_img = Path('.') / 'ATRI' / 'data' / 'img'


def b64_str_emoji(file_name: str):
    find_file = os.path.join(str(path_emoji) + '/' + file_name)
    with open(find_file, 'rb') as f:
        content = f.read()
    b64_str = base64.b64encode(content).decode()
    return b64_str

# def b64_str_img_url(url: str):
#     img_d = requests.get(url)
#     name = 'temp.jpg'
#     with open(str(path_temp_img) + '/' + name, 'wb') as f:
#         f.write(img_d.content)
#     find_img = os.path.join(str(path_temp_img) + '/' + name)
#     with open(find_img, 'rb') as f:
#         content = f.read()
#     img = ImageGrab.
#     b64_str = base64.b64encode(content).decode()
#     time.sleep(1)
#     os.remove(str(path_temp_img) + '/' + name)
#     return b64_str

def b64_str_img_path(file_name: str):
    find_file = os.path.join(str(path_img) + '/' + file_name)
    with open(find_file, 'rb') as f:
        content = f.read()
    b64_str = base64.b64encode(content).decode()
    return b64_str