from  django import  forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account
from django.utils.translation import gettext as _


class RegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, help_text="required, add a valid email.")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    def clean_phone(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'email {email} is already in use.')
  
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.get(username=username )
        except Exception as e:
            return username
        raise forms.ValidationError(_('Username %(username)s already taken') % {'username': username})
        

    

