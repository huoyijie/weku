/*!
 * @author: huoyijie
 * @file: index.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

$(safeWrap(function initIndexJS() {
    'use strict';
    var $latestVideo = $('section.preview-latest-upload-video');
    $latestVideo.find('button.preview-play').click(safeWrap(function btnPlayClick(event) {
        var player = videojs('my-player');
        player.play();
    }));
    $latestVideo.find('button.enter-playlist').click(safeWrap(function btnPlaylistClick(event) {
        window.location.href = '/video/playlist/'
    }));
}));