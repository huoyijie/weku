/*!
 * @author: huoyijie
 * @file: my-videos.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

$(safeWrap(function initMyVideosJS() {
    'use strict';
    var targetSelector = '#pagination',
        pagiInfoUrl = '/video/pagi-info/',
        pagiDataUrl = '/video/pagi-data/',
        $paginationData = $('#pagination-data'),
        success = safeWrap(function nextPageClick(json) {
            $('#op-cast')[0].dataset.castState = 'false';
            $('div[id^="video-"]').remove();
            for (var i = 0; i < json.files.length; i++) {
                var file = json.files[i];
                $paginationData.append(
                '<div id="video-' + file.id + '" class="col-4 col-md-2 mb-3 px-0">' +
                    '<div class="video-area mx-auto">' +
                    ' <img src="' + file.thumbnailUrl + '"></img>' +
                    ' <button class="btn btn-sm btn-success cast" data-id="' + file.id + '" data-cast-url="' + file.url + '">' +
                    '  <i class="glyphicon glyphicon-collapse-up"></i>' +
                    ' </button>' +
                    ' <button class="btn btn-light play" onclick="window.location.href=\'' + file.playUrl + '\'">' +
                    '  <i class="glyphicon glyphicon-play"></i>' +
                    ' </button>' +
                    '</div>' +
                '</div>'
                );
            }
        }),
        prefix = 'video';

    initPagination(targetSelector, pagiInfoUrl, pagiDataUrl, success);

    initOpCast(prefix, false);

    castButtonHandler($paginationData, prefix);
}));