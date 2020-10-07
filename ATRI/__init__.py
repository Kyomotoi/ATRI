#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from nonebot.log import logger

from utils.utils_switch import controlSwitch

file_key = Path('.') / 'key.json'

try:
    with open(file_key, 'r') as f:
        data_key = json.load(f)
except:
    data_key = {}
    data_key["API"]["LoliconAPI"] = ""
    data_key["API"]["FaceplusAPI"] = ""
    data_key["API"]["FaceplusSECRET"] = ""
    data_key["API"]["SauceNaoKEY"] = ""

    data_key["config"]["SUPERUSERS"] = [0]

if data_key["API"]["LoliconAPI"]:
    logger.info("Succeeded to load key: LoliconAPI")
else:
    logger.error("Key: LoliconAPI Can't find! URL: https://api.lolicon.app/#/setu")
    key_LoliconAPI = input("Please enter: (Enter KEY or enter 'pass' to pass)")
    if key_LoliconAPI == "pass":
        logger.error("Pass! Now func(setu) use local content.")
    data_key["API"]["LoliconAPI"] = key_LoliconAPI

if data_key["API"]["FaceplusAPI"]:
    logger.info("Succeeded to load key: FaceplusAPI")
else:
    logger.error("Key: FaceplusAPI Can't find! URL: https://www.faceplusplus.com.cn/")
    key_FaceplusAPI = input("Please enter: (Enter KEY or enter 'pass' to pass)")
    if key_FaceplusAPI == "pass":
        logger.error("Pass! This func(aichangeface) has been closed NOW!")
        controlSwitch("ai-face", False)
    data_key["API"]["FaceplusAPI"] = key_FaceplusAPI

if data_key["API"]["FaceplusSECRET"]:
    logger.info("Succeeded to load secret: FaceplusSECRET")
else:
    logger.error("Secret: FaceplusSECRET Can't find! URL: https://www.faceplusplus.com.cn/")
    secret_FaceplusSECRET = input("Please enter: (Enter SECRET or enter 'pass' to pass)")
    if secret_FaceplusSECRET == "pass":
        logger.error("Pass! This func(ai_change_face) has been closed NOW!")
        controlSwitch("ai-face", False)
    data_key["API"]["FaceplusSECRET"] = secret_FaceplusSECRET

if data_key["API"]["SauceNaoKEY"]:
    logger.info("Succeeded to load key: SauceNaoKEY")
else:
    logger.error("Key: SauceNaoKEY Can't find! URL: https://saucenao.com/")
    key_SauceNaoKEY = input("Please enter: (Enter KEY or enter 'pass' to pass)")
    if key_SauceNaoKEY == "pass":
        logger.error("Pass! This func(anime_img_search) has been closed NOW!")
        controlSwitch("anime-pic-search", False)
    data_key["API"]["SauceNaoKEY"] = key_SauceNaoKEY

with open(file_key, 'w') as f:
    f.write(json.dumps(data_key))
    f.close()

key_LoliconAPI = data_key["API"]["LoliconAPI"]
key_FaceplusAPI = data_key["API"]["FaceplusAPI"]
secret_FaceplusSECRET = data_key["API"]["FaceplusSECRET"]
key_SauceNaoKEY = data_key["API"]["SauceNaoKEY"]

config_SUPERUSERS = data_key["config"]["SUPERUSERS"]