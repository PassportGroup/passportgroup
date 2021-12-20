from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
from django.conf import settings
from oauth2client.contrib.django_util.models import CredentialsField


class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, provider=None, locale='en'):
        if not email:
            raise ValueError("User must have an email.")

        if not username:
            raise ValueError("User must have an username.")

        user = self.model(email=email, locale=locale, username = username)
        if provider and provider in ['google', 'facebook']:
            user.set_unusable_password()
            user.verified_email_at = now()

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, username):
        user = self.create_user(email=email, password=password, username=username)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename,):
    return f'profile_images/{self.pk}/{filename}'


def get_default_profile_image():
    return settings.DEFAULT_PROFILE_IMG_PATH


class Account(AbstractBaseUser):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    LINKEDIN = 'linkedin'
    PASSPORTGROUP = 'passportgroup'
    ENGLISH = 'en'
    HEBREW = 'he'

    LOCALES = (
        (ENGLISH, 'English'),
        (HEBREW, 'Hebrew'),
    )

    SIGNUP_PROVIDERS = (
        (FACEBOOK, 'facebook'),
        (GOOGLE, 'google'),
        (LINKEDIN, 'linkedin'),
        (PASSPORTGROUP, 'passportgroup'),
    )

    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True)
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=get_profile_image_filepath, blank=True, null=True, default=get_default_profile_image())
    verified_email_at = models.DateTimeField(verbose_name="verified email at", blank=True, null=True)
    signup_provider = models.CharField(max_length=15, choices=SIGNUP_PROVIDERS, default=PASSPORTGROUP)
    locale = models.CharField(max_length=2, choices=LOCALES, default=ENGLISH)
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class EmailVerificationToken(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    token = models.CharField(verbose_name="token", max_length=255)
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)


class CredentialsModel(models.Model):
    id = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE)
    credential = CredentialsField()
    task = models.CharField(max_length=80, null=True, blank=True)
    updated_time = models.CharField(max_length=80, null=True)
