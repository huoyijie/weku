/*!
 * @author: huoyijie
 * @file: my-pics.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

$(safeWrap(function initMyPicsJS() {
    'use strict';
    var targetSelector = '#pagination',
        pagiInfoUrl = '/pic/pagi-info/',
        pagiDataUrl = '/pic/pagi-data/',
        $paginationData = $('#pagination-data'),
        success = safeWrap(function nextPageClick(json) {
            $('#op-cast')[0].dataset.castState = 'false';
            $('div[id^="picture-"]').remove();
            for (var i = 0; i < json.files.length; i++) {
                var file = json.files[i];
                $paginationData.append(
                    '<div id="picture-' + file.id + '" class="col-6 col-md-2 px-0 mb-3">' +
                    '<div class="picture-area mx-auto"><a href="' + file.url + '">' +
                    ' <img src="' + file.thumbnailUrl + '"></img></a>' +
                    ' <button class="btn btn-sm btn-success cast" data-id="' + file.id + '" data-cast-url="' + file.url + '">' +
                    '  <i class="glyphicon glyphicon-collapse-up"></i>' +
                    ' </button>' +
                    '</div>' +
                    '</div>'
                );
            }
        }),
        prefix = 'picture';

    initPagination(targetSelector, pagiInfoUrl, pagiDataUrl, success);

    initOpCast(prefix, false);

    castButtonHandler($paginationData, prefix);

    // 注册blueimp.Gallery
    initGallery('#pagination-data', 'div[id^="picture-"]', false);
}));