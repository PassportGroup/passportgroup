from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    confirm_password = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if self.request.user.check_password(old_password):
            return old_password

        raise ValidationError(
            _('Your old password is incorrect.')
        )

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        new_password = self.cleaned_data['new_password']
        if confirm_password and new_password and confirm_password == new_password:
            return confirm_password

        raise ValidationError(
            _('The two passwords fields didn’t match.')
        )


class UpdateProfileForm(forms.Form):
    full_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
