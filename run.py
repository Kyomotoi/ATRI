# -*- coding:utf-8 -*-
import time
COPYRIGHT = (
    r"""
                       _____            _  ____  ____        _   
     /\               / ____|          | |/ __ \|  _ \      | |  
    /  \  _   _  __ _| |     ___   ___ | | |  | | |_) | ___ | |_ 
   / /\ \| | | |/ _` | |    / _ \ / _ \| | |  | |  _ < / _ \| __|
  / ____ \ |_| | (_| | |___| (_) | (_) | | |__| | |_) | (_) | |_ 
 /_/    \_\__, |\__,_|\_____\___/ \___/|_|\___\_\____/ \___/ \__|
           __/ |                                                 
          |___/                                                  

Copyright © 2018-2020 Kyomotoi,All Rights Reserved
Project: https://github.com/Kyomotoi/Aya
Blog: lolihub.icu
===================================================
"""
)
print(COPYRIGHT)
time.sleep(3)


from AyaBot import config
time.sleep(3)
print("开始执行主程序...RCnb!")


time.sleep(2)
from os import path
from AyaBot.plugins import module


if __name__ == '__main__':
    import nonebot
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'AyaBot', 'plugins'),
        'AyaBot.plugins')
    nonebot.run()