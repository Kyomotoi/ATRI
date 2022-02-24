from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.database.db import DB

from ATRI.utils import timestamp2datetime
from bilibili_api import user

__doc__ = """b站订阅动态助手
"""


class BilibiliDynamicSubscriptor(Service):
    def __init__(self):
        Service.__init__(self, "b站动态订阅", __doc__, rule=is_in_service("b站动态订阅"))

    async def add_subscription(self, uid: int, groupid: int) -> bool:
        async with DB() as db:
            res = await db.add_subscription(uid=uid, groupid=groupid)
            return res

    async def remove_subscription(self, uid: int, groupid: int) -> bool:
        async with DB() as db:
            res = await db.remove_subscription(query_map={'uid': uid, 'groupid': groupid})
            return res

    async def get_subscriptions(self, query_map: dict) -> list:
        async with DB() as db:
            res = await db.get_subscriptions(query_map=query_map)
            return res

    async def update_subscription_by_uid(self, uid: int, update_map: dict) -> bool:
        async with DB() as db:
            res = await db.update_subscriptions_by_uid(uid=uid, update_map=update_map)
            return res

    async def get_all_subscriptions(self) -> list:
        async with DB() as db:
            res = await  db.get_all_subscriptions()
            return res

    # bilibili network function

    async def get_upname_by_uid(self, uid: int) -> str:
        try:
            u = user.User(uid)
            info = await u.get_user_info()
            return info.get("name")
        except:
            return ""
        # {
        #     "mid": 401742377,
        #     "name": "原神",
        #     "sex": "保密",
        #     "face": "http://i2.hdslb.com/bfs/face/d2a95376140fb1e5efbcbed70ef62891a3e5284f.jpg",
        #     "face_nft": 0,
        #     "sign": "原神官方账号",
        #     "rank": 10000,
        #     "level": 6,
        #     "jointime": 0,
        #     "moral": 0,
        #     "silence": 0,
        #     "coins": 0,
        #     "fans_badge": true,
        #     "fans_medal": {
        #         "show": false,
        #         "wear": false,
        #         "medal": null
        #     },
        #     "official": {
        #         "role": 3,
        #         "title": "原神官方账号",
        #         "desc": "",
        #         "type": 1
        #     },
        #     "vip": {
        #         "type": 2,
        #         "status": 1,
        #         "due_date": 1655049600000,
        #         "vip_pay_type": 0,
        #         "theme_type": 0,
        #         "label": {
        #             "path": "",
        #             "text": "年度大会员",
        #             "label_theme": "annual_vip",
        #             "text_color": "#FFFFFF",
        #             "bg_style": 1,
        #             "bg_color": "#FB7299",
        #             "border_color": ""
        #         },
        #         "avatar_subscript": 1,
        #         "nickname_color": "#FB7299",
        #         "role": 3,
        #         "avatar_subscript_url": "http://i0.hdslb.com/bfs/vip/icon_Certification_big_member_22_3x.png"
        #     },
        #     "pendant": {
        #         "pid": 3144,
        #         "name": "原神",
        #         "image": "http://i2.hdslb.com/bfs/garb/item/6d5969a4f02fa1d4e5776072dc9f0b006478e82b.png",
        #         "expire": 0,
        #         "image_enhance": "http://i2.hdslb.com/bfs/garb/item/ff5bde4a6337140b632beffd0cbbaaf927c03ac0.webp",
        #         "image_enhance_frame": "http://i2.hdslb.com/bfs/garb/item/a1893352f03d1d6b321d504ba2ae0ecc0ea85647.png"
        #     },
        #     "nameplate": {
        #         "nid": 0,
        #         "name": "",
        #         "image": "",
        #         "image_small": "",
        #         "level": "",
        #         "condition": ""
        #     },
        #     "user_honour_info": {
        #         "mid": 0,
        #         "colour": null,
        #         "tags": []
        #     },
        #     "is_followed": false,
        #     "top_photo": "http://i0.hdslb.com/bfs/space/d64b33fe4afb1565108670f201c89c009ec236df.png",
        #     "theme": {},
        #     "sys_notice": {},
        #     "live_room": {
        #         "roomStatus": 1,
        #         "liveStatus": 0,
        #         "url": "https://live.bilibili.com/21987615",
        #         "title": "《原神》2.5版本前瞻特别节目",
        #         "cover": "http://i0.hdslb.com/bfs/live/new_room_cover/55e952e9c90c9a1c975c3ead1d81951a3be650bf.jpg",
        #         "online": 24028762,
        #         "roomid": 21987615,
        #         "roundStatus": 0,
        #         "broadcast_type": 0
        #     },
        #     "birthday": "",
        #     "school": {
        #         "name": ""
        #     },
        #     "profession": {
        #         "name": "",
        #         "department": "",
        #         "title": "",
        #         "is_show": 0
        #     },
        #     "tags": null,
        #     "series": {
        #         "user_upgrade_status": 3,
        #         "show_upgrade_window": false
        #     },
        #     "is_senior_member": 0
        # }

    async def get_recent_dynamic_by_uid(self, uid: int) -> dict:
        try:
            u = user.User(uid)
            info = await u.get_dynamics()
            return info
        except:
            return {}

    def extract_dynamics_detail(self, dynamic_list: list) -> list:
        import time
        ret = []
        for d in dynamic_list:
            pattern = {}
            desc = d["desc"]
            card = d["card"]
            type = desc["type"]

            # common 部分
            pattern["type"] = desc["type"]
            pattern["uid"] = desc["uid"]
            pattern["view"] = desc["view"]
            pattern["repost"] = desc["repost"]
            pattern["like"] = desc["like"]
            pattern["dynamic_id"] = desc["dynamic_id"]
            pattern["timestamp"] = desc["timestamp"]
            pattern["time"] = timestamp2datetime(desc["timestamp"])
            pattern["type_zh"] = ""

            # alternative 部分
            pattern["content"] = ""
            pattern["pic"] = ""

            # 根据type区分 提取content
            if type == 1:  # 转发动态
                pattern["type_zh"] = "转发动态"
                pattern["content"] = card["item"]["content"]
                pattern["pic"] = card["user"]["face"]

            elif type == 2:  # 普通动态（带多张图片）
                pattern["type_zh"] = "普通动态（附图）"
                pattern["content"] = card["item"]["description"]
                if card["item"]["pictures_count"] > 0:
                    if isinstance(card["item"]["pictures"][0], str):
                        pattern["pic"] = card["item"]["pictures"][0]
                    else:
                        pattern["pic"] = card["item"]["pictures"][0]["img_src"]

            elif type == 4:  # 普通动态（纯文字）
                pattern["type_zh"] = "普通动态（纯文字）"
                pattern["content"] = card["item"]["content"]
                # 无图片

            elif type == 8:  # 视频动态
                pattern["type_zh"] = "视频动态"
                pattern["content"] = card["dynamic"]
                pattern["pic"] = card["pic"]

            elif type == 64:  # 文章
                pattern["type_zh"] = "文章"
                pattern["content"] = card["title"] + card["summary"]
                if len(card["image_urls"]) > 0:
                    pattern["pic"] = card["image_urls"][0]

            ret.append(pattern)

        return ret

    def generate_output(self, pattern: dict) -> (str, str):
        text_part = '''【UP名称】{name}\n【动态类型】{dynamic_type}\n【动态ID】{dynamic_id}\n【时间】{time}\n【UID】{uid}\n【当前阅读次数】{view}\n【当前转发次数】{repost}\n【当前点赞次数】{like}\n【内容摘要】{content}\n'''.format(
            name=pattern["name"], dynamic_type=pattern["type_zh"], dynamic_id=pattern["dynamic_id"],
            time=pattern["time"],
            uid=pattern["uid"], view=pattern["view"], repost=pattern["repost"], like=pattern["like"],
            content=pattern["content"])
        pic_part = pattern["pic"]
        return text_part, pic_part
