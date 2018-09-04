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
import math
import os
from datetime import datetime
import subprocess
import shutil
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DeleteView, DetailView

from ffmpy import FFmpeg

from album.models import Media, Album
from video.models import Video
from weku.response import JSONResponse, response_mimetype
from weku.common_utils import serialize_video as serialize, async
from weku.video_utils import thumbnail
from weku.common_utils import cal_page_count


class VideoPagiDataView(ListView):
    model = Video

    def render_to_response(self, context, **response_kwargs):
        page = int(self.request.GET.get('page', 1))
        if page <= 0:
            page = 1

        video_list = self.get_queryset().order_by('id').reverse()
        total_count, per_page_count, page_count = cal_page_count(video_list)
        if page > page_count:
            page = 1
        cur_page_start = (page - 1) * per_page_count
        cur_page_end = np.minimum(page * per_page_count, total_count)

        files = [serialize(video) for video in video_list[cur_page_start: cur_page_end]]
        data = {'files': files,
                'page': page}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=pagidata.json'
        return response


class VideoPagiInfoView(ListView):
    model = Video

    def render_to_response(self, context, **response_kwargs):
        video_list = self.get_queryset()
        total_count, per_page_count, page_count = cal_page_count(video_list)
        data = {'total_count': total_count,
                'per_page_count': per_page_count,
                'page_count': page_count}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=paginfo.json'
        return response


class VideoUploadView(CreateView):
    model = Video
    fields = "__all__"

    @staticmethod
    def mk_video_dir(video):
        video_fp = os.path.join(video.file.storage.base_location, video.file.name)
        video_dir = video_fp.split('.')[0]
        if not os.path.exists(video_dir):
            os.mkdir(video_dir)
        return video_fp, video_dir

    def form_valid(self, form):
        self.object = form.save()
        self.join_album(form)
        video_fp, video_dir = VideoUploadView.mk_video_dir(self.object)
        self.hls_process(video_fp, video_dir)
        self.poster_process(video_fp, video_dir)
        self.video_info_process()
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
                media.type = 'video'
                media.video = self.object
                media.album = album
                media.save()

    @async
    def hls_process(self, video_fp, video_dir):
        m3u8_fp = os.path.join(video_dir, 'playlist.m3u8')
        ff = FFmpeg(
            inputs={video_fp: None},
            outputs={
                m3u8_fp:
                    '-c:a aac -c:v libx264 -strict -2 -f hls -hls_list_size 0 -hls_time 5'
            })
        print(ff.cmd)
        ff.run()

    @async
    def poster_process(self, video_fp, video_dir):
        poster_fp = os.path.join(video_dir, 'poster.jpg')
        ff = FFmpeg(inputs={video_fp: None}, outputs={
            poster_fp: '-ss 1 -f image2 -vframes 1 -y'})
        print(ff.cmd)
        ff.run()
        thumbnail(video_fp, width=80, height=150)
        thumbnail(video_fp, width=120, height=120)

    @async
    def video_info_process(self):
        video_fp = os.path.join(self.object.file.storage.base_location,
                                self.object.file.name)
        command = ['ffprobe -v quiet -print_format json -show_format %s' % video_fp]
        result = subprocess.Popen(command, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        out = result.stdout.read()
        json_info = json.loads(str(out.decode('utf-8')))
        if 'format' in json_info and 'duration' in json_info['format']:
            duration_str = json_info['format']['duration']
            duration = math.floor(float(duration_str))
        else:
            duration = 0
        if 'format' in json_info \
                and 'tags' in json_info['format'] \
                and 'creation_time' in json_info['format']['tags']:
            # 2018-06-28T07:43:21.000000Z
            take_time_str = str(json_info['format']['tags']['creation_time'])
            take_time = datetime.strptime(take_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            take_time = datetime.now()
        video = Video()
        video.id = self.object.id
        video.file = self.object.file
        video.slug = self.object.slug
        video.dirname = self.object.dirname
        video.duration = duration
        video.take_time = take_time
        video.create_time = datetime.now()
        video.save(save_file=False)


class VideoDeleteView(DeleteView):
    model = Video

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        viedo_fp = os.path.join(self.object.file.storage.base_location,
                                self.object.file.name)
        m3u8_dir = viedo_fp.split('.')[0]
        if os.path.exists(m3u8_dir):
            shutil.rmtree(m3u8_dir)
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=result.json'
        return response


class VideoPlayView(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super(VideoPlayView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        url = str(self.object.file.url).split('.')[0] + '/playlist.m3u8'
        posterUrl = str(self.object.file.url).split('.')[0] + '/poster.jpg'
        context.update({'url': url, 'posterUrl': posterUrl})
        return context


class VideoPlaylistView(ListView):
    model = Video

    @staticmethod
    def to_json_playlist(files):
        playlist = []
        for file in files:
            play = {'name': file['name'],
                    'description': file['takeTime'],
                    'sources': [{'src': file['url']}],
                    'thumbnail': [{'srcset': file['thumbnailUrl'],
                                   'type': 'image/jpeg',
                                   'media': '(min-width: 400px;)'},
                                  {'src': file['thumbnailUrl']}],
                    }
            if file['duration'] > 0:
                play['duration'] = file['duration']
            playlist.append(play)
        return playlist

    def render_to_response(self, context, **response_kwargs):
        video_list = self.get_queryset().order_by('id').reverse()
        files = [serialize(video) for video in video_list]
        data = {'playlist': VideoPlaylistView.to_json_playlist(files)}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=playlist.json'
        return response


class VideoListView(ListView):
    model = Video

    def render_to_response(self, context, **response_kwargs):
        video_list = self.get_queryset().order_by('id').reverse()
        files = [serialize(video) for video in video_list]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
