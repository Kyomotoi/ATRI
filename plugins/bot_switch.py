import re
import json
from random import choice
from pathlib import Path
from iotbot.action import Action
from iotbot import GroupMsg
from iotbot import decorators as deco
from iotbot.sugar import Text

import config_ #type: ignore


master = config_.MASTER()


@deco.not_botself
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.Content
    if re.findall(r"(开启|关闭)", msg):
        if ctx.FromUserId == master:
            msg = ctx.Content
            with open(Path('.') / 'data' / 'switch' / 'switch.json', 'r') as f:
                data = json.load(f)
            
            command = msg.split(' ', 1)
            switch = command[0]
            com = command[1]

            if switch == '开启':
                if com == 'p站搜图':
                    data["pixiv_seach_img"] = 0
                
                elif com == '画师':
                    data["pixiv_seach_author"] = 0
                
                elif com == 'P站排行榜':
                    data["pixiv_daily_rank"] = 0
                
                elif com == '好友添加':
                    data["approve_friend_add"] = 0
                
                elif com == '群邀请':
                    data["approve_invite_join_group"] = 0

                elif com == '涩图':
                    data["setu"] = 0
                
                elif com == '本子':
                    data["hbook"] = 0
                
                else:
                    pass

            elif switch == '关闭':
                if com == 'p站搜图':
                    data["pixiv_seach_img"] = 1
                
                elif com == '画师':
                    data["pixiv_seach_author"] = 1
                
                elif com == 'P站排行榜':
                    data["pixiv_daily_rank"] = 1

                elif com == '好友添加':
                    data["approve_friend_add"] = 1
                
                elif com == '群邀请':
                    data["approve_invite_join_group"] = 1

                elif com == '涩图':
                    data["setu"] = 1
                
                elif com == '本子':
                    data["hbook"] = 1
                
                else:
                    pass

                a = json.dumps(data)
                f2 = open(Path('.') / 'data' / 'switch' / 'switch.json', 'w')
                f2.write(a)
                f2.close

                Text(
                    choice(
                        [
                            '设置好啦！', '设置完成！', '好力', 'okay', '任务完成！'
                        ]
                    )
                )
        
        else:
            Text(
                choice(
                    [
                        '你我谁呢？？', '您配吗？', '恁哪位？', '仿生人是不会认错主人的！'
                    ]
                )
            )