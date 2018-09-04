#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: video_utils.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""
import logging
import os
from PIL import Image

log = logging.getLogger()


def thumbnail(fp, width=360, height=360):
    thumbnail_dir = fp.split('.')[0]
    if not os.path.exists(thumbnail_dir):
        os.mkdir(thumbnail_dir)
    poster_fp = os.path.join(thumbnail_dir, 'poster.jpg')
    if os.path.exists(poster_fp):
        with Image.open(poster_fp) as im:
            thumbnail_fp = os.path.join(thumbnail_dir,
                                        'thumbnail(%dx%d).jpg' % (width, height))
            im.thumbnail((width, height))
            im.save(thumbnail_fp)
    else:
        log.error('%s not exists!' % poster_fp)


def check_thumbnail(file, width=360, height=360):
    fp = os.path.join(file.storage.base_location, file.name)
    thumbnail_dir = fp.split('.')[0]
    assert os.path.exists(thumbnail_dir), 'video invalid.'
    thumbnail_fp = os.path.join(thumbnail_dir,
                                'thumbnail(%dx%d).jpg' % (width, height))
    if not os.path.exists(thumbnail_fp):
        thumbnail(fp, width, height)
