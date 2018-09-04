#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: views.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

import json
import os
import numpy as np
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView

from album.models import Media, Album
from weku import picture_utils
from picture.models import Picture
from weku.picture_utils import thumbnail
from weku.response import JSONResponse, response_mimetype
from weku.common_utils import serialize_picture as serialize


def cal_page_count(pic_list, per_page_count=6):
    total_count = len(pic_list)
    page_count = int(np.ceil(total_count / per_page_count))
    return total_count, per_page_count, page_count


class PicturePagiDataView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        page = int(self.request.GET.get('page', 1))
        if page <= 0:
            page = 1

        pic_list = self.get_queryset().order_by('id').reverse()
        total_count, per_page_count, page_count = cal_page_count(pic_list)
        if page > page_count:
            page = 1
        cur_page_start = (page - 1) * per_page_count
        cur_page_end = np.minimum(page * per_page_count, total_count)

        cur_page_pic_list = [
            pic for pic in pic_list[cur_page_start: cur_page_end]
        ]

        files = [serialize(p) for p in cur_page_pic_list]
        data = {'files': files,
                'page': page}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=pagidata.json'
        return response


class PicturePagiInfoView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        pic_list = self.get_queryset()
        total_count, per_page_count, page_count = cal_page_count(pic_list)
        data = {'total_count': total_count,
                'per_page_count': per_page_count,
                'page_count': page_count}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=paginfo.json'
        return response


class PictureUploadView(CreateView):
    model = Picture
    fields = "__all__"

    def pic_process(self):
        fname = os.path.join(self.object.file.storage.base_location,
                             self.object.file.name)
        picture_utils.read_img_and_correct_exif_orientation(fname)
        thumbnail(fname)

    def form_valid(self, form):
        self.object = form.save()
        self.join_album(form)
        self.pic_process()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400,
                            content_type='application/json')

    def join_album(self, form):
        try:
            album_id = int(form.data['albumId'])
        except:
            album_id = 0
            pass
        if album_id > 0:
            album = Album.objects.filter(id=album_id).first()
            if album is not None:
                media = Media()
                media.type = 'picture'
                media.picture = self.object
                media.album = album
                media.save()


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=result.json'
        return response
