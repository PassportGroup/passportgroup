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

# Create your views here.


def index_view(request):
    return render_inertia(request, 'Index',
        props={
            'listings': [],
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            phone_number = request.POST.get('phone_number').replace(' ', '')
            password = request.POST.get('password')
            user = authenticate(request, phone=phone_number, password=password)
            _next = request.POST.get('next')
            if user is not None and user.is_active:
                login(request, user)
                return redirect(_next if _next != '' else '/')
            else:
                share_flash(request, error=_("These credentials do not match our records."))
        else:
            share_flash(request, errors=json.loads(form.errors.as_json()))

    return render_inertia(request, 'Auth/Login')


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))



# def verify_phone_view(request):
#     context = {}
#
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         form = VerifyPhoneForm(data)
#
#         if form.is_valid():
#             code = int(data.get('code'))
#             phone = data.get('phone').replace(' ','')
#             user = get_object_or_404(User, phone = phone)
#             otp = get_object_or_404(OTP, user = user)
#             otp_type = request.session.get('otp_type')
#
#             redirect_next = data.get('redirect_next', str(reverse('login')))
#
#             try:
#                 assert timezone.now() < otp.created_at + timedelta(minutes = 5), 'code-expired'
#                 assert int(otp.code) == code, 'invalid-code'
#
#                 del request.session['otp_type']
#                 del request.session['phone_number']
#
#                 if otp_type == 'verify-phone':
#                     user.verified_phone_at = timezone.now()
#                     user.save()
#                     otp.delete()
#
#                     return JsonResponse(
#                         {
#                             'message': _('Phone number verified successfully'),
#                             'redirect_next': redirect_next
#                         }
#                     )
#
#                 if otp_type == 'reset-password':
#                     token = default_token_generator.make_token(user)
#                     uid = urlsafe_base64_encode(force_bytes(user.pk))
#
#                     return JsonResponse(
#                         {
#                             'message': '',
#                             'redirect_next': str(reverse('password.reset', kwargs = {'uidb64': uid, 'token': token}))
#                         }
#                     )
#
#             except AssertionError as e:
#                 if e.args:
#                     if str(e.args[0]) == 'invalid-code':
#                         context = {'message': _('Invalid Code')}
#                     else:
#                         otp.delete()
#                         context = {'message': _('Your otp code has expired')}
#         else:
#             context = {'message': _('invalid form data')}
#
#     response = JsonResponse(context)
#     response.status_code = 400
#     return response

#
# def verify_email_view(request, *args, **kwargs):
#     assert 'uidb64' in kwargs and 'token' in kwargs
#     token = kwargs['token']
#
#     try:
#         # urlsafe_base64_decode() decodes to bytestring
#         uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
#         user = None
#
#     email_token = get_object_or_404(EmailVerificationToken, email=user.email)
#
#     if email_token:
#         if timezone.now() < (email_token.created_at + timedelta(hours=1)) and email_token.token == token:
#             user.verified_email_at = timezone.now()
#             user.save()
#             share_flash(request, success=_('Email verified successfully'))
#             email_token.delete()
#             return redirect(reverse('settings'))
#         else:
#             email_token.delete()
#             share_flash(request, error=_('Your verification link has expired'))
#
#     return redirect(reverse('login'))


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

    return HttpResponseRedirect(request.META['HTTP_REFERER']) if request.META['HTTP_REFERER'] else reverse(redirect('home'))


def privacy_policy(request):

    return render_inertia(
        request,
        'PrivacyPolicy'
    )


def terms_of_service(request):

    return render_inertia(
        request,
        'TermsOfService'
    )