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
from apps.core.services.gmail_api.common import gmail_authenticate, search_messages
from apps.core.services.gmail_api.read_emails import read_message
from datetime import datetime, timedelta

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
            email = request.POST.get('email').replace(' ', '')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            _next = request.POST.get('next')
            if user is not None and user.is_active:
                login(request, user)
                return redirect(_next if _next != '' else '/')
            else:
                share_flash(request, error=_("These credentials do not match our records."))
        else:
            share_flash(request, errors=json.loads(form.errors.as_json()))

    return render_inertia(request, 'Index')


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))


def mail_listing_view(request):
    query = request.GET.get('query', None)
    start_date_query = request.GET.get('start_date', None) or datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_date_query = request.GET.get('end_date', None)
    page = request.GET.get('page', 1)

    begin_date = datetime.strptime(start_date_query, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_date = begin_date + timedelta(14)
    if end_date_query:
        end_date = datetime.strptime(end_date_query, '%Y-%m-%dT%H:%M:%S.%fZ')

    try:
        gmail_service = gmail_authenticate()
        # Build query from this
        query = "after:" + begin_date.strftime('%Y/%m/%d') + " before:" + end_date.strftime('%Y/%m/%d')
        mails = search_messages(gmail_service, query)
        final_mails = []
        for mail in mails:
            data = read_message(gmail_service, mail)
            if data:
                # process data on drive
                print(data)
                final_mails.append(data)
    except Exception:
        final_mails = [
            {
                'thread_id': '17c12b2801d9e9a7',
                'snippet': 'This is a copy of a security alert sent to m.laurent@waspito.com. muarachmann@gmail.com is the recovery email for this account. If you don&#39;t recognize this account, disconnect it. Your email was',
                'is_approved': True,
                'date': 'Thu, 23 Sep 2021 12:47:39 GMT',
                'message_id': '<lle25t-sS_LSlEVcIbqSGw@notifications.google.com>',
                'subject': 'Your email is now a recovery email for m.laurent@waspito.com'
             },
            {
                'thread_id': '17c12b24b432a919',
                'snippet': 'Verify your recovery email Google received a request to use muarachmann@gmail.com as a recovery email for Google Account m.laurent@waspito.com. Use this code to finish setting up this recovery email:',
                'is_approved': False,
                'message_id': '<000000000000737c4905cca90855@google.com>',
                'date': 'Thu, 23 Sep 2021 12:47:26 +0000',
                'subject': 'Email verification code: 546595'
            },
            {
                'thread_id': '17bdebb761b067a2',
                'snippet': 'Hello here is the access to your portal insurance.waspito.com -- MUA N. LAURENT: Lead Software Engineer WASPITO (Health without a step) m.laurent@waspito.com',
                'is_approved': True,
                'date': 'Mon, 13 Sep 2021 11:37:01 +0100',
                'message_id': '<CAB8+b9dDqVgwG73aAEwsGz2LcbsKi0b7xFUqQmEPc+DSPeps0g@mail.gmail.com>',
                'subject': 'Insurance Platform'
            },
            {
                'thread_id': '17bdebb761b067a2',
                'snippet': 'Hello here is the access to your portal insurance.waspito.com -- MUA N. LAURENT: Lead Software Engineer WASPITO (Health without a step) m.laurent@waspito.com',
                'is_approved': True,
                'date': 'Mon, 13 Sep 2021 11:37:01 +0100',
                'message_id': '<CAB8+b9dDqVgwG73aAEwsGz2LcbsKi0b7xFUqQmEPc+DSPeps0g@mail.gmail.com>',
                'subject': 'Insurance Platform'
            }
        ]

    # paginate data
    mails_obj, links = paginate(
        objects=final_mails,
        current_url=request.build_absolute_uri(),
        items_per_page=50,
        current_page=page
    )
    return render_inertia(
        request,
        'Dashboard/Mails/Index',
        props={
            'mails': final_mails,
            'query': query,
            'start_date': start_date_query,
            'end_date': end_date_query,
            'links': links
        }
    )


def mail_details_view(request):
    return render_inertia(request, 'Dashboard/Mails/Detail')



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