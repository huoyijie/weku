#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: views.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from video.models import Video
from weku import settings
from weku.common_utils import serialize_video as serialize, get_client_ip
from video.views import cal_page_count
from weku.response import JSONResponse, response_mimetype


class WekuIndexView(ListView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super(WekuIndexView, self).get_context_data(**kwargs)
        file = {}
        total_count = 0
        video_list = self.get_queryset().order_by('id').reverse()
        if len(video_list) > 0:
            video = video_list.first()
            file = serialize(video)
            total_count, _, _ = cal_page_count(video_list)
        data = {'file': file,
                'total_count': total_count}
        context.update(data)
        return context


@login_required
def debug(request):
    switch = request.GET.get('switch')
    client_ip = get_client_ip(request)
    if switch is not None and switch == 'toggle':
        if client_ip in settings.INTERNAL_IPS:
            settings.INTERNAL_IPS.remove(client_ip)
        else:
            settings.INTERNAL_IPS.append(client_ip)
    return JSONResponse({'code': 0,
                         'isDebug': client_ip in settings.INTERNAL_IPS},
                        mimetype=response_mimetype(request))
