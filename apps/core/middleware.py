import random
import string

from inertia.views import render_inertia
from django.conf import settings

DEBUG = settings.DEBUG


class TriggerErrorsResponseAndReturnInertiaResponse:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        status = response.status_code
        if status in [404, 403, 500, 503] and not DEBUG:
            return render_inertia(
                request,
                'Errors/Index',
                props={
                    'status': status
                }
            )

        return response


class XForwardedForMiddleware:
    """
    Set REMOTE_ADDR if it's missing because of a reverse proxy (nginx + gunicorn) deployment.
    https://stackoverflow.com/questions/34251298/empty-remote-addr-value-in-django-application-when-using-nginx-as-reverse-proxy
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            parts = request.META['HTTP_X_FORWARDED_FOR'].split(',', 1)
            request.META['HTTP_X_PROXY_REMOTE_ADDR'] = request.META['REMOTE_ADDR']
            request.META['REMOTE_ADDR'] = parts[0]

        return response


class GenerateUserCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id_cookie = request.COOKIES.get(settings.USER_ID_COOKIE_NAME)
        response = self.get_response(request)

        if not user_id_cookie:
            alphabets = list(string.ascii_letters + string.ascii_lowercase)
            random.shuffle(alphabets)
            uid = ''.join(alphabets[0:20])

            response.set_cookie(
                settings.USER_ID_COOKIE_NAME, uid,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )

        return response


class UserLanguagePreferenceMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        django_lang_from_cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, None)
        response = self.get_response(request)

        if not django_lang_from_cookie:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, request.LANGUAGE_CODE,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )

        else:
            for cookie in request.META['HTTP_COOKIE'].split(';'):
                if settings.LANGUAGE_COOKIE_NAME in cookie:
                    try:
                        path_lang = request.META.get('PATH_INFO').split('/')[1]
                        cookie_lang = cookie.split('=')[1]
                        if path_lang in ['en', 'he'] and cookie_lang != path_lang:
                            response.set_cookie(
                                settings.LANGUAGE_COOKIE_NAME, path_lang,
                                max_age=settings.LANGUAGE_COOKIE_AGE,
                                path=settings.LANGUAGE_COOKIE_PATH,
                                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                                secure=settings.LANGUAGE_COOKIE_SECURE,
                                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                            )

                        break

                    except (Exception, IndexError):
                        pass

        return response
