import os

from django.contrib.messages import constants as messages  # import Django flash messages
from django.core.mail import send_mail  #  Python provides a mail sending interface via the smtplib module

from my_settings import Mine


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vzmsim#g#58z^-k($-9zf37myziy*fcpy$)6247i-wy@%e5@5q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',  # translates numbers and dates into a human readable format.

    'accounts.apps.AccountsConfig',

    'bootstrap4',  # bootstrap4 import

    'django_filters',  # django_filters import

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# location of all 'static' files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cms/static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'cdn_static')

# creates 'static' folder in the root dir (CMS) after running collectstatic
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# images and videos
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'cms/static/img')


# message config  https://docs.djangoproject.com/en/2.2/ref/contrib/messages/
MESSAGE_TAGS = {
    messages.ERROR: 'alert-danger',  # value is equal to the bootstrap class of 'alert-danger'
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# host: EMAIL_HOST
# port: EMAIL_PORT
# username: EMAIL_HOST_USER
# password: EMAIL_HOST_PASSWORD
# use_tls: EMAIL_USE_TLS
# use_ssl: EMAIL_USE_SSL