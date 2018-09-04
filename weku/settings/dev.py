#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: dev.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""
from .base import *

SECRET_KEY = 'o7w+bfw*vkutog!evl1ige(1gj7&*p)&t^=k9$u#g_mc4r8%cr'
DEBUG = True
WSGI_APPLICATION = 'weku.wsgi.sentry'
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'debug_toolbar',
    'video',
    'picture',
    'album',
    'dlnacast',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
# 配置Raven开启Sentry Error Report(需确保已正确安装Sentry)
RAVEN_CONFIG = {
    'dsn': 'http://b7461a5dc13548bf84205ed0394c50fa:953ec0cc75164bfca29ce1f0c452c718@192.168.31.53:9000/2',
    'release': '1.0.0',
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'weku-pro',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['default', 'console', 'sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s\t%(levelname)s\t%(pathname)s('
                      '%(funcName)s:%(lineno)s)\t%(message)s\t'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/webapps/weku/weku-django.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['default', 'console'],
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['default', 'console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['default', 'console'],
            'propagate': False,
        },
    },
}
