from marshmallow import Schema, fields, validate
from django.db.models import Q
from apps.utils import k_number, round_rate
from django.conf import settings
from django.utils.timesince import timesince as timesince_
from django.db.models import Avg, Count
from apps.account.models import Account
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class UserSchema(Schema):
    email = fields.Email()
    username = fields.Str()
    date_joined = fields.DateTime()
    last_login = fields.DateTime()
    is_active = fields.Boolean()
    profile_image = fields.Method('get_profile_image')
    signup_provider = fields.Str()
    unread_messages = fields.Method('count_unread_messages')
    verify_email = fields.Function(lambda obj: True if obj.verified_email_at else False)
    is_admin = fields.Function(lambda obj: obj.is_admin or obj.is_superuser)
    roles = fields.Method('get_user_roles')
    permissions = fields.Method('get_user_roles')

    def get_profile_image(self, obj):
        return settings.MEDIA_URL + str(obj.profile_image)

    def get_user_roles(self, obj):
        return ['super_admin', 'admin']

    def get_user_permissions(self, obj):
        return ['process_emails']

    def count_unread_messages(self, obj):
        return 1200


class ProfileSchema(Schema):
    user = fields.Str()
