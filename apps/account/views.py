from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.decorators  import login_required
from inertia.views import render_inertia
from inertia.share import share_flash
from apps.core.services.mail import Mail
import os, json
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.core.serializers import NotificationSettingSchema
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.utils.translation import gettext as _
from apps.core.forms import ChangePasswordForm, UpdateProfileForm

@login_required
def settings_view(request):
    error = False
    success = ''
    if request.method == 'POST':
        picture = request.FILES.get('picture', None)
        user = get_object_or_404(User, username = request.user.username)
        if picture:
            if user.profile_image and user.profile_image.url.split('/')[-1] != settings.DEFAULT_PROFILE_IMG_PATH.split('/')[-1]:
                 user.profile_image.storage.delete(user.profile_image.name)

            user.profile_image = picture
            user.save()
        else:
            form = UpdateProfileForm(request.POST)

            if form.is_valid():
                full_name = request.POST.get('full_name')
                username = request.POST.get('username')
                email = request.POST.get('email')

                if email != request.user.email:
                    if not User.objects.filter(email = email).exists():
                        if username != request.user.username:
                            if not User.objects.filter(username = username).exists():
                                user.email = email
                                user.username = username
                                user.verified_email_at = None
                                user.full_name = full_name
                                user.save()
                                Mail.send_email_verification(request, user)
                                share_flash(request, success = _('We sent you an email to verify your profile'))
                            else:
                                share_flash(request, error = _('Username %(username)s already taken') % {'username': username})
                        else:
                            user.email = email
                            user.full_name = full_name
                            user.verified_email_at = None
                            user.save()
                            Mail.send_email_verification(request, user)
                            share_flash(request, success = _('We sent you an email to verify your profile'))
                    else:
                        share_flash(request, error = _('Email %(email)s already taken') % {'email': email})
                else:
                    if username != user.username:
                        if not User.objects.filter(username = username).exists():
                            user.username = username
                            user.full_name = full_name
                            user.save()
                            success = _('Profile updated successfully')
                        else:
                            error = True
                            share_flash(request, error = _('Username %(username)s already taken') % {'username': username})

                    if not error:
                        user.full_name = full_name
                        user.save()
                        success = _('Profile updated successfully')

                        if not user.verified_email_at:
                            Mail.send_email_verification(request, user)
                            success = _('We sent you an email to verify your profile')

                        share_flash(request, success = success)


            else:
                share_flash(request, errors = json.loads(form.errors.as_json()))

    return render_inertia(
        request,
        'User/Settings/ProfileInformation'
    )


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request = request)

        if form.is_valid():
            new_password = request.POST.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            share_flash(request, success=_('Password change successfully'))
            return redirect(reverse('login'))

        else:
            share_flash(request, errors = json.loads(form.errors.as_json()))

    return render_inertia(
        request,
        'User/Settings/ChangePassword'
    )

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        if request.user.check_password(password):
            request.user.is_active = False
            request.user.save()

            share_flash(request, success = _('Account delete successfully'))
            return redirect(reverse('logout'))

        else:
            share_flash(request, error = _('Your password is incorrect'))

    return render_inertia(
        request,
        'User/Settings/DeleteAccount'
    )


@login_required
def security_view(request):
    if request.method == 'POST':
        two_factor_auth = request.POST.get('two_factor_auth', None)

        if two_factor_auth is not None:
            request.user.two_factor_auth = two_factor_auth
            request.user.save()

    return render_inertia(
        request,
        'User/Settings/Security',
    )