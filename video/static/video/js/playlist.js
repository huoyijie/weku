/*!
 * @author: huoyijie
 * @file: playlist.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

$(safeWrap(function initPlaylistJS() {
    'use strict';
    $.get('/video/playlist-data/', {}, safeWrap(function getPlaylistCallback(data) {
        var player = videojs('my-player');
        player.playlist(data.playlist);
        // Play through the playlist automatically.
        player.playlist.autoadvance(0);
        // Initialize the plugin and build the playlist!
        player.playlistUi();
    }));
}));