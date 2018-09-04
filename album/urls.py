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

from album.views import AlbumCreateView, AlbumDeleteView, AlbumPagiDataView, \
    AlbumPagiInfoView, AlbumDetailView, AlbumListView, MediaDeleteView, MediaMoreDataView
from weku.common_utils import ajax_login_required

urlpatterns = [
    path('my-albums/',
         login_required(TemplateView.as_view(template_name='album/my-albums.html',
                        extra_context={'thisPage': 'my-albums'})),
         name='album-my-albums'),
    path('create/',
         ajax_login_required(AlbumCreateView.as_view()),
         name='album-create'),
    path('delete/<int:pk>',
         ajax_login_required(AlbumDeleteView.as_view()),
         name='album-delete'),
    path('pagi-data/',
         ajax_login_required(AlbumPagiDataView.as_view()),
         name='album-pagination-data'),
    path('pagi-info/',
         ajax_login_required(AlbumPagiInfoView.as_view()),
         name='album-pagination-info'),
    path('detail/<int:pk>',
         login_required(AlbumDetailView.as_view(template_name='album/detail.html',
                        extra_context={'thisPage': 'detail'})),
         name='album-detail'),
    path('list/',
         ajax_login_required(AlbumListView.as_view()),
         name='album-list'),
    path('media/delete/<int:pk>',
         ajax_login_required(MediaDeleteView.as_view()),
         name='media-delete'),
    path('<int:pk>/more-data/',
         ajax_login_required(MediaMoreDataView.as_view()),
         name='media-more-data'),
]
