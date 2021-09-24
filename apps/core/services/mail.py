from django.core.mail import EmailMultiAlternatives
import os
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from apps.utils import generate_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from apps.notifications import tasks


class Mail:
    MAIL_FROM = os.getenv('MAIL_FROM_ADDRESS')

    @staticmethod
    def send_mail(subject_template_name, email_template_name, context, from_email, to_email, request, html_content=False):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(
            template_name=subject_template_name,
            context=context,
            request=request
        )

        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(
            template_name=email_template_name,
            context=context,
            request=request
        )

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_content:
            email_message.content_subtype = 'html'

        email_message.send(fail_silently=True)

    @staticmethod
    def send_email_verification(request, user):
        from apps.account.models import EmailVerificationToken

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        token = generate_token(64)
        email_verification_obj = EmailVerificationToken.objects.filter(email=user.email)

        if email_verification_obj.exists():
            email_verification_obj.delete()

        EmailVerificationToken.objects.create(email=user.email, token=token)

        context = {
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'username': user.username,
            'token': token,
            'protocol': "https" if request.is_secure() else "http",
        }

        Mail.send_mail(
            "mail/registration/verify_email_subject.txt",
            "mail/registration/verify_email.html",
            context,
            Mail.MAIL_FROM,
            user.email,
            request,
            True
        )

    @staticmethod
    def send_id_verification_mail_to_admin(request):
        current_site = Site.objects.get_current()
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'domain': domain,
            'site_name': site_name,
            'username': request.user.username,
            'protocol': "https" if request.is_secure() else "http",
        }

        tasks.send_email_notifications.delay(
            "notifications/subjects/en/id_verification.html",
            "notifications/email/en/id_verification.html",
            context,
            os.getenv('MAIL_SUPPORT_ADDRESS', 'hello@passportgroup.il.co'),
            600,
            Mail.MAIL_FROM,
        )

    @staticmethod
    def send_reset_email_link(user, request):
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': "https" if request.is_secure() else "http",
        }

        Mail.send_mail(
            "mail/registration/password_reset_subject.txt",
            "mail/registration/password_reset_email.html",
            context,
            Mail.MAIL_FROM,
            user.email,
            request
        )
