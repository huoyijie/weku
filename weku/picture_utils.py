#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: picture_utils.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

import logging
import exifread
import os
from PIL import Image


def read_img_and_correct_exif_orientation(path):
    with open(path, 'rb') as f:
        im = Image.open(path)
        tags = exifread.process_file(f, details=False)
        if "Image Orientation" in tags.keys():
            orientation = tags["Image Orientation"]
            logging.debug("Orientation: %s (%s)", orientation, orientation.values)
            val = orientation.values
            if 5 in val:
                val += [4, 8]
            if 7 in val:
                val += [4, 6]
            if 3 in val:
                logging.debug("Rotating by 180 degrees.")
                im = im.transpose(Image.ROTATE_180)
            if 4 in val:
                logging.debug("Mirroring horizontally.")
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if 6 in val:
                logging.debug("Rotating by 270 degrees.")
                im = im.transpose(Image.ROTATE_270)
            if 8 in val:
                logging.debug("Rotating by 90 degrees.")
                im = im.transpose(Image.ROTATE_90)
        im.save(path)
        im.close()


def thumbnail(fp, width=360, height=360):
    thumbnail_dir = fp.split('.')[0]
    if not os.path.exists(thumbnail_dir):
        os.mkdir(thumbnail_dir)
    with Image.open(fp) as im:
        thumbnail_fp = os.path.join(thumbnail_dir,
                                    'thumbnail(%dx%d).jpg' % (width, height))
        im.thumbnail((width, height))
        im.save(thumbnail_fp)


def check_thumbnail(file, width=360, height=360):
    fp = os.path.join(file.storage.base_location, file.name)
    thumbnail_dir = fp.split('.')[0]
    thumbnail_fp = os.path.join(thumbnail_dir, 'thumbnail(%dx%d).jpg' % (width, height))
    if not os.path.exists(thumbnail_fp):
        thumbnail(fp, width, height)
