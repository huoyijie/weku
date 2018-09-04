#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: docker.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

from .base import *

with open(os.path.join(BASE_DIR, 'weku', 'settings', 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()
DEBUG = False
MEDIA_ROOT = os.path.join('/data', 'weku', 'media')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('/data', 'weku', 'weku-db.sqlite3'),
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['default', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s\t%(levelname)s\t%(pathname)s('
                      '%(funcName)s:%(lineno)s)\t%(message)s\t'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/data/applogs/weku/weku-django.log',
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
    },
}