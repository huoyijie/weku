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

from video.views import VideoUploadView, VideoDeleteView, VideoListView, VideoPlayView, \
    VideoPlaylistView, VideoPagiDataView, VideoPagiInfoView
from weku.common_utils import ajax_login_required

urlpatterns = [
    path('my-videos/',
         login_required(TemplateView.as_view(template_name='video/my-videos.html',
                        extra_context={'thisPage': 'my-videos'})),
         name='video-my-videos'),
    path('pagi-data/',
         ajax_login_required(VideoPagiDataView.as_view()),
         name='video-pagination-data'),
    path('pagi-info/',
         ajax_login_required(VideoPagiInfoView.as_view()),
         name='video-pagination-info'),
    path('upload/',
         ajax_login_required(VideoUploadView.as_view()),
         name='video-upload'),
    path('delete/<int:pk>',
         ajax_login_required(VideoDeleteView.as_view()),
         name='video-delete'),
    path('play/<int:pk>',
         login_required(VideoPlayView.as_view(template_name='video/play.html',
                        extra_context={'thisPage': 'play'})),
         name='video-play'),
    path('playlist/',
         login_required(TemplateView.as_view(template_name='video/playlist.html',
                        extra_context={'thisPage': 'playlist'})),
         name='video-index'),
    path('playlist-data/',
         ajax_login_required(VideoPlaylistView.as_view()),
         name='video-playlist-data'),
    path('view/',
         ajax_login_required(VideoListView.as_view()),
         name='video-view'),
]
