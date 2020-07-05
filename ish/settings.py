"""
Django settings for ish project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x2-2pv$8c5_y8f+n^*58h0kk7--00^5(#m6)2b8ty$i1cwj(!$'

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
    'stark.apps.StarkConfig',
    'rbac.apps.RbacConfig',
    'wxapi.apps.App01Config',
    'backstage.apps.BackstageConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middlewares.rbac.RbacMiddleware'
]

ROOT_URLCONF = 'ish.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'ish.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# create database ish default charset utf8mb4;
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ish',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'POST': 3306,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False              # 转时区


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticAll')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "rbac", "static"),
    os.path.join(BASE_DIR, "stark", "static"),
    os.path.join(BASE_DIR, "xadmin", "static")
]

MINA_APP = {
    'appid': '',        # 小程序appid
    'appkey': '',       # 小程序appkey
}

# AUTH_USER_MODEL = "wxapi.Customer"   # 继承django自带的用户表时使用

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

URL = 'http://192.168.3.46:8000'


# ######################## rbac相关配置 #############################
USER_MODEL_PATH = "backstage.models.UserInfo"

MENU_SESSION_KEY = 'menu_session_key'
PERMISSION_SESSION_KEY = 'permi_key'


PERMISSION_VALID_URL = [
    '/backstage/.*',
    '/wxapi/.*',
    '/media/.*',
    '/admin/.*',
    '/static/.*',
    '/robots\.txt/*'
]

STATIC_FILES = [
    '\.css/*$',
    '\.js/*$',
    '\.png|jpg|svg/*$',
    '\.ttf/*'

]
