import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load environment file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

# Mail configurations
if os.getenv('APP_ENV') == 'production':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('MAIL_HOST', 'smtp.gmail.com')
    EMAIL_HOST_USER = os.getenv('MAIL_USERNAME', '')
    DEFAULT_FROM_EMAIL = os.getenv('MAIL_FROM_ADDRESS', 'info@passportgroup.co.il')
    EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASSWORD', '')  # past the key or password app here
    EMAIL_PORT = os.getenv('MAIL_PORT', 587)
    EMAIL_USE_TLS = os.getenv('MAIL_ENCRYPTION', os.getenv('MAIL_ENCRYPTION') == 'True')
    EMAIL_TIMEOUT = 60

else:
    DEFAULT_FROM_EMAIL = os.getenv('MAIL_FROM_ADDRESS', 'info@passportgroup.co.il')
    EMAIL_TIMEOUT = 60
    EMAIL_HOST = os.getenv('MAIL_HOST', 'localhost')
    EMAIL_PORT = os.getenv('MAIL_PORT', 1025)

if os.getenv('APP_ENV') == 'local':
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = ['5.189.177.4', 'ctrl.passportgroup.co.il']


GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = os.path.join(BASE_DIR, 'gmail_credentials.json')

PASSPORT_BASE_EMAIL = os.getenv('GMAIL_ID')
PASSPORT_FROM_EMAIL = os.getenv('FROM_GMAIL_ID')

AUTH_USER_MODEL = 'account.Account'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'home'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'apps.dashboard',
    'apps.account',
    'apps.core',
    'channels',
    'rest_framework',
    'inertia',
    'djangomix',
    'debug_toolbar',
    'meta',
    'js_routes',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.core.middleware.TriggerErrorsResponseAndReturnInertiaResponse',
    'apps.core.middleware.UserLanguagePreferenceMiddleware',
    'apps.core.middleware.GenerateUserCookieMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.XForwardedForMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'passportgroup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.app_description',
                'apps.core.context_processors.app_keywords',
                'apps.core.context_processors.app_name',
            ],
        },
    },
]

WSGI_APPLICATION = 'passportgroup.wsgi.application'

ASGI_APPLICATION = 'passportgroup.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DB_CONNECTION = os.getenv('DB_CONNECTION') if os.getenv('DB_CONNECTION') else 'postgresql'

if DB_CONNECTION == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql' if DB_CONNECTION == 'postgresql' else 'django.db.backends.mysql',
            'NAME': os.getenv('DB_DATABASE'),
            'USER': os.getenv('DB_USERNAME'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'use_unicode': True,
            },
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

prefix_default_language = True

LANGUAGES = [
    ('he', _('Hebrew')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Tells inertia-django which base template you want to use
# index.html is provided in the boilerplate
INERTIA_TEMPLATE = 'base.html'

# default user share on each response
INERTIA_SHARE = 'apps.core.apps.share_auth'

JS_ROUTES_INCLUSION_LIST = [
    'home',
    'login',
    'logout',
    'locale.set',
    'privacy.policy',
    'terms.of.service',


    # dashboard routes
    'dashboard.index',
    'dashboard.google.auth',
    'dashboard.google.callback',
    'dashboard.mails.index',
    'dashboard.mails.detail',
    'dashboard.tasks.index',
    'dashboard.tasks.detail',
    'dashboard.tasks.update',

]


INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'EXTRA_SIGNALS': [
        # 'apps.notifications.signals.passportgroup_notify',
    ],
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CELERY STUFF
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Douala'

APP_DESCRIPTION = _("Process emails passportgroup")
APP_KEYWORDS = _("gmail, drive, pdf, python, passportgroup")
USER_ID_COOKIE_NAME = 'pg_uuid'

DEFAULT_PROFILE_IMG_PATH = 'default_profile.png'

# META SETTINGS
META_SITE_NAME = 'Passport Group'
META_DEFAULT_KEYWORDS = "gmail, email, drive, processing,, files".split(',')
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_TITLE_TAG = True
META_USE_SITES = True
META_SITE_PROTOCOL = 'https' if os.getenv('APP_ENV') == 'production' else 'http'
