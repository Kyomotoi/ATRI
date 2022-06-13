from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Subscription(Model):
    uid = fields.IntField()
    group_id = fields.IntField()
    up_nickname = fields.TextField(null=True)
    last_update = fields.DatetimeField(default=datetime.fromordinal(1))

    def __str__(self) -> str:
        return f"[{self.uid}|{self.group_id}|{self.up_nickname}|{self.last_update}]"
