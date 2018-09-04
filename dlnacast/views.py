#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: views.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

import logging
import threading as thd
from urllib.parse import unquote
import upnpclient
from django.utils.translation import ugettext as _
from django.views import View

from dlnacast.upnp_utils import didl_meta_data
from weku.response import JSONResponse, response_mimetype

log = logging.getLogger()


class SSDP:
    devices = []

    @staticmethod
    def discover():
        SSDP.devices = upnpclient.discover()
        # print(SSDP.get_devices())
        ssdp_daemon = thd.Timer(30, SSDP.discover)
        ssdp_daemon.setDaemon(True)
        ssdp_daemon.start()

    @staticmethod
    def get_devices():
        ret = []
        for device in SSDP.devices:
            if hasattr(device, 'AVTransport'):
                ret.append({'manufacturer': device.manufacturer,
                            'friendly_name': device.friendly_name,
                            'location': device.location})
        return ret

    @staticmethod
    def get_one():
        devs = []
        for device in SSDP.devices:
            if hasattr(device, 'AVTransport'):
                devs.append(device)
        for device in devs:
            if device.manufacturer == 'LEBO':
                return device
        for device in devs:
            if device.manufacturer == 'Xiaomi':
                return device
        if len(devs) > 0:
            return devs[0]
        else:
            return None

    @staticmethod
    def get_one_by_friendly_name(friendly_name):
        for device in SSDP.devices:
            if hasattr(device, 'AVTransport') and device.friendly_name == friendly_name:
                return device
        return SSDP.get_one()

    @staticmethod
    def get_one_by_manufacturer(manufacturer):
        for device in SSDP.devices:
            if hasattr(device, 'AVTransport') and device.manufacturer == manufacturer:
                return device
        return SSDP.get_one()


# start discover thread in bg.
SSDP.discover()


class DLNACastDevicesView(View):

    def get(self, request, *args, **kwargs):
        data = {'devices': SSDP.get_devices()}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=devices.json'
        return response


class DLNACastView(View):

    def get(self, request, *args, **kwargs):
        cast_url = request.GET['castUrl'] if 'castUrl' in request.GET else ''
        if cast_url != '':
            cast_url = unquote(cast_url, 'utf-8')
            friendly_name = request.GET['device'] if 'device' in request.GET else ''
            file_suffix = cast_url.lower().split('.')[-1]
            is_picture = (file_suffix in ['jpg', 'jpeg', 'png', 'gif'])
            if friendly_name == '' and is_picture:
                device = SSDP.get_one_by_manufacturer('Xiaomi')
            else:
                device = SSDP.get_one_by_friendly_name(friendly_name)
            if device is not None:
                try:
                    meta_data = didl_meta_data(cast_url) if is_picture else ''
                    device.AVTransport.SetAVTransportURI(
                        InstanceID=0,
                        CurrentURI=cast_url,
                        CurrentURIMetaData=meta_data)
                    data = {'code': 0}
                except:
                    log.error(_('DLNA Device offline.'))
                    data = {'code': -3, 'msg': _('DLNA Device offline.')}
            else:
                log.error(_('DLNA Device not found.'))
                data = {'code': -2, 'msg': _('DLNA Device not found.')}
        else:
            log.error(_('Cast Url is blank.'))
            data = {'code': -1, 'msg': _('Cast Url is blank.')}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=result.json'
        return response
