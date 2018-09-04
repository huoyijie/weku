#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: urls.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from picture.views import PictureUploadView, PictureDeleteView, PicturePagiDataView, \
    PicturePagiInfoView
from weku.common_utils import ajax_login_required

urlpatterns = [
    path('my-pics/',
         login_required(TemplateView.as_view(template_name='picture/my-pics.html',
                        extra_context={'thisPage': 'my-pics'})),
         name='picture-my-pics'),
    path('upload/',
         ajax_login_required(PictureUploadView.as_view()),
         name='picture-upload'),
    path('delete/<int:pk>',
         ajax_login_required(PictureDeleteView.as_view()),
         name='picture-delete'),
    path('pagi-data/',
         ajax_login_required(PicturePagiDataView.as_view()),
         name='picture-pagination-data'),
    path('pagi-info/',
         ajax_login_required(PicturePagiInfoView.as_view()),
         name='picture-pagination-info'),
]
