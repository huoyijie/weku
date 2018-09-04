#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: urls.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

from django.urls import path
from dlnacast.views import DLNACastDevicesView, DLNACastView
from weku.common_utils import ajax_login_required

urlpatterns = [
    path('devices/',
         ajax_login_required(DLNACastDevicesView.as_view()),
         name='dlnacast-devices'),
    path('cast/',
         ajax_login_required(DLNACastView.as_view()),
         name='dlnacast-cast'),
]
