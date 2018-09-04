#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: models.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

import uuid

from datetime import datetime

import os
import shutil
from django.db import models


def upload_to(video, filename):
    gen_filename = uuid.uuid1().hex
    ext = str(filename).split('.')[-1].lower()
    video.file.name = '%s.%s' % (gen_filename, ext)
    video.slug = video.file.name
    return os.path.join(video.dirname, 'videos', video.file.name)


class Video(models.Model):
    class Meta:
        db_table = 'wk_video'

    dirname = models.CharField(max_length=20)
    """ffmpeg -i IMG_1158.MOV -c:v libx264 -c:a aac -strict -2 -f hls -hls_list_size 0 -hls_time 5 IMG_1158.m3u8"""
    file = models.FileField(upload_to=upload_to)
    slug = models.SlugField(max_length=50, blank=True)
    duration = models.IntegerField(blank=True)
    take_time = models.DateTimeField(blank=True)
    create_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('video-upload', )

    def save(self, save_file=True, *args, **kwargs):
        if save_file:
            self.create_time = datetime.now()
            self.take_time = datetime.now()
            self.duration = 0
        super(Video, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        viedo_fp = os.path.join(self.file.storage.base_location,
                                self.file.name)
        m3u8_dir = viedo_fp.split('.')[0]
        if os.path.exists(m3u8_dir):
            shutil.rmtree(m3u8_dir)
        self.file.delete(False)
        super(Video, self).delete(*args, **kwargs)
