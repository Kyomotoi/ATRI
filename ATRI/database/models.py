from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class BilibiliSubscription(Model):
    uid = fields.IntField()
    group_id = fields.IntField()
    up_nickname = fields.TextField(null=True)
    last_update = fields.DatetimeField(default=datetime.fromordinal(1))

    class Meta:
        app = "bilibili"


class TwitterSubscription(Model):
    tid = fields.IntField()
    group_id = fields.IntField()
    name = fields.TextField(null=True)
    screen_name = fields.TextField(null=True)
    last_update = fields.DatetimeField(default=datetime.fromordinal(1))

    class Meta:
        app = "twitter"


class ThesaurusStoragor(Model):
    _id = fields.TextField()
    matcher = fields.TextField(null=True)
    result = fields.JSONField(null=True)
    need_at = fields.IntField(null=True)
    m_type = fields.IntField(null=True)
    group_id = fields.IntField(null=True)
    operator = fields.TextField(null=True)
    operator_id = fields.IntField(null=True)
    update_time = fields.DatetimeField(null=True)
    is_vote = fields.IntField(null=True)
    vote_list = fields.JSONField(null=True)

    class Meta:
        app = "ts"


class ThesaurusAuditList(Model):
    _id = fields.TextField()
    matcher = fields.TextField(null=True)
    result = fields.JSONField(null=True)
    need_at = fields.IntField(null=True)
    m_type = fields.IntField(null=True)
    group_id = fields.IntField(null=True)
    operator = fields.TextField(null=True)
    operator_id = fields.IntField(null=True)
    update_time = fields.DatetimeField(null=True)
    is_vote = fields.IntField(null=True)
    vote_list = fields.JSONField(null=True)

    class Meta:
        app = "tal"


class RssRsshubSubcription(Model):
    _id = fields.TextField()
    group_id = fields.IntField(null=True)
    title = fields.TextField(null=True)
    raw_link = fields.TextField(null=True)
    rss_link = fields.TextField(null=True)
    discription = fields.TextField(null=True)
    update_time = fields.DatetimeField(default=datetime.fromordinal(1))

    class Meta:
        app = "rrs"


class RssMikananiSubcription(Model):
    _id = fields.TextField()
    group_id = fields.IntField(null=True)
    title = fields.TextField(null=True)
    rss_link = fields.TextField(null=True)
    discription = fields.TextField(null=True)
    update_time = fields.DatetimeField(default=datetime.fromordinal(1))

    class Meta:
        app = "rms"
