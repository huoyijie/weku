#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: common_utils.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""
import socket
from threading import Thread
import numpy as np
import mimetypes
import re
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from album.models import Media
from weku.picture_utils import check_thumbnail
from weku.video_utils import check_thumbnail as video_check_thumbnail


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize_picture(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    check_thumbnail(obj)
    result = {
        'url': obj.url,
        'name': order_name(obj.name),
        'mimetype': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': str(obj.url).split('.')[0] + '/thumbnail(360x360).jpg',
        'size': obj.size,
        'deleteUrl': reverse('picture-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
        'id': instance.pk,
        'pictureId': instance.pk,
        'contentType': 'image/*',
    }
    return result


def serialize_video(instance, file_attr='file'):
    """serialize -- Serialize a video instance into a dict.

    instance -- Video instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    url = str(obj.url).split('.')[0] + '/playlist.m3u8'
    poster_url = str(obj.url).split('.')[0] + '/poster.jpg'
    thumbnail_url = poster_url.replace('poster.jpg', 'thumbnail(360x360).jpg')
    video_check_thumbnail(obj)
    result = {
        'url': url,
        'name': order_name(obj.name),
        'mimetype': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': thumbnail_url,
        'size': obj.size,
        'deleteUrl': reverse('video-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
        'playUrl': reverse('video-play', args=[instance.pk]),
        'posterUrl': poster_url,
        'id': instance.pk,
        'videoId': instance.pk,
        'contentType': 'video/*',
    }
    if instance.duration > 0:
        result['duration'] = instance.duration
    if instance.take_time is not None:
        result['takeTime'] = instance.take_time.strftime('%m/%d/%Y %H:%M:%S')
    if instance.create_time is not None:
        result['createTime'] = instance.create_time.strftime('%m/%d/%Y %H:%M:%S')
    return result


def serialize(media):
    result = {}
    if media.type == 'picture':
        result = serialize_picture(media.picture)
    elif media.type == 'video':
        result = serialize_video(media.video)
    else:
        assert media.type != 'picture' and media.type != 'video', 'media.type invalid.'
    result['id'] = media.id
    result['type'] = media.type
    result['deleteUrl'] = reverse('media-delete', args=[media.id])
    return result


def serialize_album(album):
    media_count = Media.objects.filter(album_id=album.id).count()
    cover_pic = Media.objects.filter(album_id=album.id,
                                     type='picture').order_by('id').reverse().first()
    cover_url = ''
    if cover_pic is not None:
        check_thumbnail(cover_pic.picture.file)
        furl = cover_pic.picture.file.url
        cover_url = str(furl).split('.')[0] + '/thumbnail(360x360).jpg'
    default_cover = 'holder.js/100px100p?theme=thumb&bg=55595c&fg=eceeef&text=ALBUM'
    return {'id': album.id,
            'name': album.name,
            'holderCoverUrl': default_cover,
            'coverUrl': cover_url,
            'mediaCount': media_count,
            'deleteUrl': reverse('album-delete', args=[album.id])}


def async(func):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


def cal_page_count(obj_list, per_page_count=6):
    total_count = len(obj_list)
    page_count = int(np.ceil(total_count / per_page_count))
    return total_count, per_page_count, page_count


def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_host_ip():
    s, ip = None, ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s is not None:
            s.close()
    return ip
