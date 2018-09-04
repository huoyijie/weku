/*!
 * @author: huoyijie
 * @file: play.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

$(safeWrap(function initPlayJS() {
   'use strict';
   $.get('/dlnacast/devices/', {}, safeWrap(function getDLNADevices(data) {
        for (var i = 0; i < data.devices.length; i++) {
            $('div.dlna-cast').append('<a href="#" class="btn btn-dark col-6 cast">'
                + data.devices[i].friendly_name + '</a>')
        }
   }));

   $('div.dlna-cast').click('a.cast', safeWrap(function btnCastClick(event) {
       event.preventDefault();
       var player = videojs('my-player');
       player.pause();
       _dlnacast(this.dataset.castUrl, event.target.text);
   }));
}));