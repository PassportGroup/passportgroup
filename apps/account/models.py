from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.timezone import now
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class AccountManager(BaseUserManager):

    def create_user(self, username, email=None, phone=None, full_name=None, password=None, provider=None, locale=None):
        if not username:
            raise ValueError("User must have a username.")

        user = self.model(phone=phone, username = username, full_name=full_name, email=email, locale=locale)
        if provider and provider in ['google', 'facebook']:
            user.set_unusable_password()
            user.verified_email_at = now()
            user.signup_provider = provider

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, username, password):
        user = self.create_user(phone=phone, username=username, password=password)
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
        (PASSPORTGROUP, 'passportgroup'),
    )

    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True)
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    full_name = models.CharField(verbose_name='full name', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name="phone", max_length=14, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=get_profile_image_filepath, blank=True, null=True, default=get_default_profile_image())
    hide_email = models.BooleanField(default=True)
    verified_phone_at = models.DateTimeField(verbose_name="verified phone at", blank=True, null=True)
    verified_email_at = models.DateTimeField(verbose_name="verified email at", blank=True, null=True)
    verified_user_at = models.DateTimeField(verbose_name="verified user at", blank=True, null=True)
    signup_provider = models.CharField(max_length=15, choices=SIGNUP_PROVIDERS, default=PASSPORTGROUP)
    two_factor_auth = models.BooleanField(default=False)
    locale = models.CharField(max_length=2, choices=LOCALES, default=ENGLISH)
    uid = models.CharField(max_length=50, blank=True, null=True)
    objects = AccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class EmailVerificationToken(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    token = models.CharField(verbose_name="token", max_length=255)
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
