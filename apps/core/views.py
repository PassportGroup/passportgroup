import json
from inertia.views import render_inertia
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from inertia.share import share_flash
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from datetime import timedelta
from django.utils import timezone
from .forms import LoginForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q, ExpressionWrapper, DateTimeField
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from apps.utils import *
from django.utils.translation import gettext as _
from apps.core.services.gmail_api.common import gmail_authenticate, search_messages, get_mail
from apps.core.services.gmail_api.read_emails import read_message
from datetime import datetime, timedelta


# Create your views here.
def index_view(request):
    return render_inertia(request, 'Index')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = request.POST.get('email').replace(' ', '')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            _next = request.POST.get('next')
            if user is not None and user.is_active:
                login(request, user)
                return redirect(_next if _next != '' else '/dashboard')
            else:
                share_flash(request, error=_("These credentials do not match our records."))
        else:
            share_flash(request, errors=json.loads(form.errors.as_json()))

    return render_inertia(request, 'Index')


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))


def set_locale_view(request):
    if request.method == 'POST':
        next_url = request.POST.get('next')
        locale = request.POST.get('locale')

        if locale:
            for lang in settings.LANGUAGES:
                if locale == lang[0]:
                    if request.user.is_authenticated:
                        request.user.locale = locale
                        request.user.save()

                    response = redirect(next_url)
                    response.set_cookie(
                        settings.LANGUAGE_COOKIE_NAME, locale,
                        max_age=settings.LANGUAGE_COOKIE_AGE,
                        path=settings.LANGUAGE_COOKIE_PATH,
                        domain=settings.LANGUAGE_COOKIE_DOMAIN,
                        secure=settings.LANGUAGE_COOKIE_SECURE,
                        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                    )
                    return response

    return HttpResponseRedirect(request.META['HTTP_REFERER']) if request.META['HTTP_REFERER'] \
        else reverse(redirect('home'))


def privacy_policy(request):

    return render_inertia(request, 'PrivacyPolicy')


def terms_of_service(request):

    return render_inertia(request, 'TermsOfService')
