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
import numpy as np
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DeleteView, DetailView

from album.models import Album, Media
from picture.models import Picture
from video.models import Video
from weku.common_utils import serialize, serialize_album
from weku.response import JSONResponse, response_mimetype


def cal_page_count(the_list, per_page_count=6):
    total_count = len(the_list)
    page_count = int(np.ceil(total_count / per_page_count))
    return total_count, per_page_count, page_count


class AlbumPagiDataView(ListView):
    model = Album

    def render_to_response(self, context, **response_kwargs):
        page = int(self.request.GET.get('page', 1))
        if page <= 0:
            page = 1

        album_list = self.get_queryset().order_by('id').reverse()
        total_count, per_page_count, page_count = cal_page_count(album_list)
        if page > page_count:
            page = 1
        cur_page_start = (page - 1) * per_page_count
        cur_page_end = np.minimum(page * per_page_count, total_count)

        cur_page_album_list = [
            album for album in album_list[cur_page_start: cur_page_end]
        ]
        albums = [serialize_album(p) for p in cur_page_album_list]
        data = {'albums': albums, 'page': page}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=pagidata.json'
        return response


class AlbumPagiInfoView(ListView):
    model = Album

    def render_to_response(self, context, **response_kwargs):
        album_list = self.get_queryset()
        total_count, per_page_count, page_count = cal_page_count(album_list)
        data = {'total_count': total_count,
                'per_page_count': per_page_count,
                'page_count': page_count}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=paginfo.json'
        return response


class AlbumCreateView(CreateView):
    model = Album
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        data = {'code': 0}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=reslut.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400,
                            content_type='application/json')


class AlbumDeleteView(DeleteView):
    model = Album

    def delete(self, request, *args, **kwargs):
        album = self.get_object()
        media_list = Media.objects.filter(album_id=album.id)
        picture_ids = []
        video_ids = []
        for media in media_list:
            assert media.type in ['video', 'picture'], 'media.type invalid.'
            if media.type == 'picture':
                # media.picture.delete()
                picture_ids.append(media.picture_id)
            elif media.type == 'video':
                # media.video.delete()
                video_ids.append(media.video_id)
        # first delete medias
        media_list.delete()
        # then delete pictures and videos
        Picture.objects.filter(id__in=picture_ids).delete()
        Video.objects.filter(id__in=video_ids).delete()
        # last delete album
        album.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=result.json'
        return response


class AlbumDetailView(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        album = self.get_object()
        media_list = Media.objects.filter(album_id=album.id).order_by('id').reverse()
        medias = [serialize(media) for media in media_list]
        data = {'album': album,
                'medias': medias}
        context.update(data)
        return context


class AlbumListView(ListView):
    model = Album

    def render_to_response(self, context, **response_kwargs):
        album_list = self.get_queryset().order_by('id').reverse()
        albums = [{'id': album.id, 'name': album.name} for album in album_list]
        data = {'albums': albums}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=albums.json'
        return response


class MediaDeleteView(DeleteView):
    model = Media

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        assert self.object.type in ['video', 'picture'], 'media.type invalid.'
        if self.object.type == 'picture':
            self.object.picture.delete()
        elif self.object.type == 'video':
            self.object.video.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=result.json'
        return response


class MediaMoreDataView(DetailView):
    model = Album

    def render_to_response(self, context, **response_kwargs):
        page = int(self.request.GET.get('page', 1))
        if page <= 0:
            page = 1
        album = self.get_object()
        media_list = Media.objects.filter(album_id=album.id).order_by('id').reverse()

        total_count, per_page_count, page_count = cal_page_count(media_list,
                                                                 per_page_count=8)
        if page > page_count:
            medias = []
        else:
            cur_page_start = (page - 1) * per_page_count
            cur_page_end = np.minimum(page * per_page_count, total_count)
            medias = [serialize(media) for media in media_list[cur_page_start: cur_page_end]]
        data = {'medias': medias, 'pageCount': page_count}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=media-more-data.json'
        return response
