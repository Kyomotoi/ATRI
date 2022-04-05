from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.database.db import DB
from ATRI.utils import timestamp2datetime

import json
import aiohttp
import os
import re
import asyncio
from typing import Any
from operator import itemgetter


__session_pool = {}


def get_api(field: str) -> dict:
    """
    获取 API。

    Args:
        field (str): API 所属分类，即 data/api 下的文件名（不含后缀名）

    Returns:
        dict, 该 API 的内容。
    """
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f"{field.lower()}.json")
    )
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())
    else:
        return dict()


API: dict = get_api("user")


def get_session():
    """
    获取当前模块的 aiohttp.ClientSession 对象，用于自定义请求

    Returns:
        aiohttp.ClientSession
    """
    loop = asyncio.get_event_loop()
    session = __session_pool.get(loop, None)
    if session is None:
        session = aiohttp.ClientSession(loop=loop)
        __session_pool[loop] = session

    return session


async def bilibili_request(
    method: str,
    url: str,
    params: dict = dict(),
    data: Any = None,
    no_csrf: bool = False,
    json_body: bool = False,
    **kwargs,
) -> dict:
    """
    向接口发送请求。

    Args:
        method     (str)                 : 请求方法。
        url        (str)                 : 请求 URL。
        params     (dict, optional)      : 请求参数。
        data       (Any, optional)       : 请求载荷。
        no_csrf    (bool, optional)      : 不要自动添加 CSRF。
        json_body (bool, optional) 载荷是否为 JSON

    Returns:
        接口未返回数据时，返回 None，否则返回该接口提供的 data 或 result 字段的数据。
    """

    method = method.upper()

    # 使用 Referer 和 UA 请求头以绕过反爬虫机制
    DEFAULT_HEADERS = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0",
    }
    headers = DEFAULT_HEADERS

    if params is None:
        params = {}

    # 自动添加 csrf
    if not no_csrf and method in ["POST", "DELETE", "PATCH"]:
        if data is None:
            data = {}
        data["csrf"] = ""
        data["csrf_token"] = ""

    # jsonp

    if params.get("jsonp", "") == "jsonp":
        params["callback"] = "callback"

    config = {
        "method": method,
        "url": url,
        "params": params,
        "data": data,
        "headers": headers,
        "cookies": "",
    }

    config.update(kwargs)

    if json_body:
        config["headers"]["Content-Type"] = "application/json"
        config["data"] = json.dumps(config["data"])

    session = get_session()

    async with session.request(**config) as resp:

        # 检查状态码
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise Exception(e.message)

        # 检查响应头 Content-Length
        content_length = resp.headers.get("content-length")
        if content_length and int(content_length) == 0:
            return dict()

        # 检查响应头 Content-Type
        content_type = resp.headers.get("content-type")

        # 不是 application/json
        if content_type.lower().index("application/json") == -1:  # type: ignore
            raise Exception("响应不是 application/json 类型")

        raw_data = await resp.text()
        resp_data: dict = dict()

        if "callback" in params:
            # JSONP 请求
            resp_data = json.loads(re.match("^.*?({.*}).*$", raw_data, re.S).group(1))  # type: ignore
        else:
            # JSON
            resp_data = json.loads(raw_data)

        # 检查 code
        code = resp_data.get("code", None)

        if code is None:
            raise Exception("API 返回数据未含 code 字段")

        if code != 0:
            msg = resp_data.get("msg", None)
            if msg is None:
                msg = resp_data.get("message", None)
            if msg is None:
                msg = "接口未返回错误信息"
            raise Exception(msg)

        real_data = resp_data.get("data", None)
        if real_data is None:
            real_data = resp_data.get("result", None)
        return real_data


class User:
    """
    b站用户相关
    """

    def __init__(self, uid: int):
        """
        Args:
            uid        (int)                 : 用户 UID
        """
        self.uid = uid

        self.__self_info = None  # 暂时无用

    async def get_user_info(self) -> dict:
        """
        获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["info"]
        params = {"mid": self.uid}
        return await bilibili_request("GET", url=api["url"], params=params)

    async def get_dynamics(self, offset: int = 0, need_top: bool = False):
        """
        获取用户动态。

        Args:
            offset (str, optional):     该值为第一次调用本方法时，数据中会有个 next_offset 字段，
                                        指向下一动态列表第一条动态（类似单向链表）。
                                        根据上一次获取结果中的 next_offset 字段值，
                                        循环填充该值即可获取到全部动态。
                                        0 为从头开始。
                                        Defaults to 0.
            need_top (bool, optional):  显示置顶动态. Defaults to False.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["dynamic"]
        params = {
            "host_uid": self.uid,
            "offset_dynamic_id": offset,
            "need_top": 1 if need_top else 0,
        }
        data: dict = await bilibili_request("GET", url=api["url"], params=params)
        # card 字段自动转换成 JSON。
        if "cards" in data:
            for card in data["cards"]:
                card["card"] = json.loads(card["card"])
                card["extend_json"] = json.loads(card["extend_json"])
        return data


class BilibiliDynamicSubscriptor(Service):
    def __init__(self):
        Service.__init__(self, "b站动态订阅", "b站订阅动态助手", rule=is_in_service("b站动态订阅"))

    async def add_subscription(self, uid: int, groupid: int) -> bool:
        async with DB() as db:
            res = await db.add_subscription(uid=uid, groupid=groupid)
            return res

    async def remove_subscription(self, uid: int, groupid: int) -> bool:
        async with DB() as db:
            res = await db.remove_subscription(
                query_map={"uid": uid, "groupid": groupid}
            )
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
            res = await db.get_all_subscriptions()
            return res

    # bilibili network function

    async def get_upname_by_uid(self, uid: int) -> str:
        try:
            u = User(uid)
            info: dict = await u.get_user_info()
            return info.get("name")
        except:
            return ""

    async def get_recent_dynamic_by_uid(self, uid: int) -> dict:
        try:
            u = User(uid)
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
                pattern["content"] = card["title"] + card["dynamic"]
                pattern["pic"] = card["pic"]

            elif type == 64:  # 文章
                pattern["type_zh"] = "文章"
                pattern["content"] = card["title"] + card["summary"]
                if len(card["image_urls"]) > 0:
                    pattern["pic"] = card["image_urls"][0]

            ret.append(pattern)
        ret = sorted(ret, key=itemgetter("timestamp"))
        return ret

    def generate_output(self, pattern: dict) -> tuple:
        # 限制摘要的字数
        abstractLimit = 40
        text_part = """【UP名称】{name}\n【动态类型】{dynamic_type}\n【时间】{time}\n【内容摘要】{content}\n""".format(
            name=pattern["name"],
            dynamic_type=pattern["type_zh"],
            time=pattern["time"],
            content=pattern["content"][:abstractLimit],
        )
        pic_part = pattern["pic"]
        return text_part, pic_part
