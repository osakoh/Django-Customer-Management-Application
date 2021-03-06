import os

from django.contrib.messages import constants as messages  # import Django flash messages
#  Python provides a mail sending interface via the smtplib module

from my_settings import Configure

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Configure.s_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

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

    'django.contrib.postgres',  # PostgreSQL

    'storages',  # storages
    # 'boto3'  # 'boto3',  # boto3

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

# SQLite3 configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# PostgreSQL configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': Configure.postgres,
        'HOST': 'cms-db.caxfwbgqaxyz.eu-west-2.rds.amazonaws.com',
        'PORT': '5432',
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

# STATIC_URL = '/static/'

# location of all 'static' files
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'cms/static')
# ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'cdn_static')

# creates 'static' folder in the root dir (CMS) after running collectstatic
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# images and videos
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'cms/static/img')

# message config  https://docs.djangoproject.com/en/2.2/ref/contrib/messages/
MESSAGE_TAGS = {
    messages.ERROR: 'alert-danger',  # value is equal to the bootstrap class of 'alert-danger'
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
}

# smtp-config
EMAIL_BACKEND = Configure.backend

EMAIL_HOST = Configure.host
EMAIL_PORT = Configure.port
EMAIL_USE_TLS = Configure.uts
EMAIL_HOST_USER = Configure.usr
EMAIL_HOST_PASSWORD = Configure.pwd

# S3 BUCKETS
AWS_ACCESS_KEY_ID = Configure.access_key
AWS_SECRET_ACCESS_KEY = Configure.secret_key
AWS_STORAGE_BUCKET_NAME = Configure.bucket_name
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'  # None

AWS_LOCATION = 'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cms/static')
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'cms/static/img')

"""
S3 BUCKETS 
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

AWS_S3_FILE_OVERWRITE = ''
AWS_DEFAULT_ACL = ''
DEFAULT_FILE_STORAGE = ''

<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>


[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "http://www.example1.com"
        ],
        "ExposeHeaders": []
    },
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "http://www.example2.com"
        ],
        "ExposeHeaders": []
    },
    {
        "AllowedHeaders": [],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
"""
