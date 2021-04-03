"""
Django settings for tena project.

Generated by 'django-admin startproject' using Django 3.1.7.
"""

from pathlib import Path

import django.conf.locale
from decouple import config
from dj_database_url import parse as db_url
from django.conf import global_settings
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1'] # Need for debug_toolbar

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Additional

    # Third party

    'smart_selects',
    'django_extensions',
    'debug_toolbar',

    # Local

    'ausers.apps.AusersConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tena.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tena.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' / BASE_DIR / 'db.sqlite3',
        cast=db_url
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGES = (
    ('am', _('Amharic')),
    ('am-or', _('Oromiffa')),
    ('en', _('English')),
)

EXTRA_LANG_INFO = {
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': u"አማርኛ"
    },
    'am-or': {
        'bidi': False,
        'code': 'am_or',
        'name': 'Oromiffa',
        'name_local': u"Oromiffa"
    }

}

LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)

django.conf.locale.LANG_INFO = LANG_INFO

TIME_ZONE = 'Africa/Addis_Ababa'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Authentication conf

AUTH_USER_MODEL = 'ausers.User'


# Smart Select conf

USE_DJANGO_JQUERY = True
