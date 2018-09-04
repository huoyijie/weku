#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: urls.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.conf.urls.static import static
import debug_toolbar
from django.views.generic import RedirectView, TemplateView
from django.views.i18n import JavaScriptCatalog

from weku import settings
from weku.views import WekuIndexView, debug

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',
         login_required(WekuIndexView.as_view(template_name='index.html',
                        extra_context={'thisPage': 'home'})),
         name='video-index'),
    url(r'^video/', include('video.urls')),
    url(r'^pic/', include('picture.urls')),
    url(r'^album/', include('album.urls')),
    url(r'^dlnacast/', include('dlnacast.urls')),
    path('', lambda x: HttpResponseRedirect('/index/')),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    path('switch-lang/', TemplateView.as_view(template_name='switch-lang.html',
                                              extra_context={'thisPage': 'switch-lang'}),
         name='switch-lang'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('debug/', debug, name='debug'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ]
if settings.SILKY:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk')), ]
