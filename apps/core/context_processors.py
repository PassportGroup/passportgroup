import os
from django.utils.translation import gettext as _
from django.conf import settings


def app_description(request):
    return {'app_description': settings.APP_DESCRIPTION}


def app_keywords(request):
    return {'app_keywords': settings.APP_KEYWORDS}


def app_name(request):
    return {'app_name': _(os.getenv('APP_NAME'))}