#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: wsgi.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""
import os
from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weku.settings")

application = get_wsgi_application()

sentry = Sentry(application)
