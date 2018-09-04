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


def upload_to(picture, filename):
    gen_filename = uuid.uuid1().hex
    ext = str(filename).split('.')[-1].lower()
    picture.file.name = '%s.%s' % (gen_filename, ext)
    picture.slug = picture.file.name
    return os.path.join(picture.dirname, 'pictures', picture.file.name)


class Picture(models.Model):
    class Meta:
        db_table = 'wk_picture'

    dirname = models.CharField(max_length=20)
    file = models.FileField(upload_to=upload_to)
    slug = models.SlugField(max_length=50, blank=True)
    take_time = models.DateTimeField(blank=True)
    create_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('picture-upload', )

    def save(self, *args, **kwargs):
        self.create_time = datetime.now()
        # fixme
        self.take_time = datetime.now()
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        fp = os.path.join(self.file.storage.base_location, self.file.name)
        thumbnail_dir = fp.split('.')[0]
        if os.path.exists(thumbnail_dir):
            shutil.rmtree(thumbnail_dir)
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
