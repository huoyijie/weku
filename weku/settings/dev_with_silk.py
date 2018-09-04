#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: dev_with_silk.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""
from .dev import *

SILKY = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'silk',
    'raven.contrib.django.raven_compat',
    'debug_toolbar',
    'video',
    'picture',
    'album',
    'dlnacast',
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
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

# SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True
'''SILKY_DYNAMIC_PROFILING = [{
    'module': 'django.views.generic',
    'function': 'View.dispatch'
}]'''
SILKY_AUTHENTICATION = True
SILKY_META = True
