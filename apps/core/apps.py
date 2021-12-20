from django.apps import AppConfig
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from inertia.share import share
from .serializers import UserSchema
from apps.core.services.google_api import common


def current_user(request):
    is_anonymous = isinstance(get_user(request), AnonymousUser)
    if is_anonymous:
        return None

    user_schema = UserSchema(only=("username", "email", "profile_image", "date_joined", "is_admin", "roles",
                                   "permissions", "unread_messages"))
    print(user_schema)
    return user_schema.dump(get_user(request))


def share_auth(request):
    if not request.user.is_anonymous:
        share(request, "google_access", common.check_credential(request))
    share(request, "auth", current_user(request))


class CoreConfig(AppConfig):
    name = 'apps.core'


