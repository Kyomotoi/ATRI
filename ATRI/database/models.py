"""
    定义SQLITE数据库的关系模式（表）
    数据库采用了tortoise orm，可以很好地支持异步
"""

from tortoise.models import Model
from tortoise import fields
from datetime import datetime

# b站订阅表
class Subscription(Model):
    uid = fields.IntField(pk=True)  # up的uid
    groupid = fields.IntField()  # 群号
    nickname = fields.TextField(null=True)  # 订阅up的名称
    last_update = fields.DatetimeField(
        default=datetime.fromordinal(1)
    )  # 上一条动态更新时间 默认0001-01-01 00:00:00

    def __str__(self):
        return "[{nickname}|{uid}|{groupid}]".format(
            nickname=self.nickname, uid=self.uid, groupid=self.groupid
        )
