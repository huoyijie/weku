#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: admin.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

from django.contrib import admin

from video.models import Video

admin.site.register(Video)
