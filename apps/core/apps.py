import time

from django.apps import AppConfig
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from inertia.share import share
from .serializers import UserSchema


def current_user(request):
    
    is_anonymous = isinstance(get_user(request), AnonymousUser)
    if is_anonymous:
        return None

    user_schema = UserSchema(only=("username", "email", "full_name", "profile_image", "date_joined", "phone", "is_verified", "unread_messages", "is_admin", "verification", "verify_phone", "two_factor_auth"))
    return user_schema.dump(get_user(request))


def share_auth(request):
    share(request, "auth", current_user(request))


class CoreConfig(AppConfig):
    name = 'core'


