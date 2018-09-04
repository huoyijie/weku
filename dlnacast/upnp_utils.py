#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: upnp_utils.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""


def didl_meta_data(url, album_name=''):
    meta_data = \
        '<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" \
                    xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" \
                    xmlns:dc="http://purl.org/dc/elements/1.1/" \
                    xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" \
                    xmlns:sec="http://www.sec.co.kr/"> \
            <item id="filePath" parentID="0" restricted="1"> \
                <upnp:class>object.item.imageItem</upnp:class> \
                <dc:title></dc:title> \
                <dc:creator></dc:creator> \
                <upnp:artist></upnp:artist> \
                <upnp:albumArtURI></upnp:albumArtURI> \
                <upnp:album>{album_name}</upnp:album> \
                <res protocolInfo="http-get:*:image/jpeg:DLNA.ORG_PN=JPEG_LRG;DLNA.ORG_OP=01;DLNA.ORG_FLAGS=01700000000000000000000000000000"> \
                    {url} \
                </res> \
            </item> \
        </DIDL-Lite>'
    return meta_data.format(album_name=album_name, url=url)
