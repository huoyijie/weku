#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: models.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

from django.db import models

from picture.models import Picture
from video.models import Video


class Album(models.Model):
    """ID=10,000,000代表默认相册，需要在初次使用时由初始化脚本自动创建."""
    class Meta:
        db_table = 'wk_album'

    name = models.CharField(max_length=20)


class Media(models.Model):
    class Meta:
        db_table = 'wk_media'

    type = models.CharField(max_length=20)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, null=True)
    picture = models.OneToOneField(Picture, on_delete=models.CASCADE, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
