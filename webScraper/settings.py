"""
Django settings for webScraper project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from django.conf import settings
# from 
# import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qz#beug2k2y_x^gyr&cpl+zt()4l33=9-uoq8dp56(-vh!rovr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.herokuapp.com', 'http://127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scraper',
    'django_celery_beat'
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

ROOT_URLCONF = 'webScraper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'webScraper.wsgi.application'

# env = environ.Env()
# environ.Env.read_env()
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('EMAIL_HOST'),
#         'USER': 'dB_productionflow',
#         'PASSWORD': 'dB_productionflow',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd311qon3vbrun7',
#         'USER': 'uruwllzzddbgey',
#         'PASSWORD': 'b29e9143ea4c6a8787e8877ce40bee57d92e543a7fac7eb8eaed566f6b81fca8',
#         'HOST': 'ec2-54-76-43-89.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }


DATABASES = {
    'default': {}
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ['EMAIL_HOST']
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True  rvybtgntrgzmvuuy
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD =os.environ['EMAIL_HOST_PASSWORD']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-pulse.com'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@streamysubscriptions.com'
EMAIL_HOST_PASSWORD ='tafabalewa1omoobaloluwa2com'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'dashboard/'

DATABASE_URI="postgres://uruwllzzddbgey:b29e9143ea4c6a8787e8877ce40bee57d92e543a7fac7eb8eaed566f6b81fca8@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/d311qon3vbrun7"

# celery settings
#localhost
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
# heroku
# CELERY_IMPORTS = ("tasks", )
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0')

# CELERY_RESULT_BACKEND = 'amqp://localhost:5672'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "scraper.tasks.scrape_mydash",
        "schedule": 900.0,
    }
}
