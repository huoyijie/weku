/*!
 * @author: huoyijie
 * @file: detail.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

function _showUploadPopup() {
    $('body').removeClass('h-auto').addClass('h-100');
    $('#input-file').avgrund({
        width: 200,
        height: 120,
        holderClass: 'my-file-upload-popup',
        showClose: false,
        showCloseText: 'close',
        closeByDocument: false,
        closeByEscape: false,
        onBlurContainer: '.container',
        template:
        '<div>' +
        ' <h6>' + gettext('Upload Progress') + '<span>(0%)</span></h6>' +
        ' <div id="progress" class="progress">' +
        '  <div class="progress-bar bg-success"></div>' +
        ' </div>' +
        ' <div id="files" class="files">' +
        '  <small></small>' +
        ' </div>' +
        '</div>',
        openOnEvent: false
    });
}

function _hideUploadPopup() {
    $('.files small').text('Upload Finished.');
    setTimeout(safeWrap(function hideProgressTimeoutCallback() {
        $('.avgrund-active').removeClass('avgrund-active');
        $('.avgrund-popin').remove();
        $('body').removeClass('h-100').addClass('h-auto');
        window.location.reload();
    }), 1000);
}

function _updateProgressBar(loaded, total) {
    var progress = parseInt(loaded / total * 100, 10);
    $('.progress .progress-bar').css(
        'width',
        progress + '%'
    );
    $('.my-file-upload-popup h6 span').text('(' +
        progress + '%)');
    if (progress === 100) {
        $('.files small').text(gettext('Processing...'));
    }
}

function _initFileupload(targetSelector, uploadUrl, acceptFileTypes, maxFileSize, messages) {
    var $fileupload = $(targetSelector);
    $fileupload.fileupload({
        url: uploadUrl,
        dataType: 'json',
        acceptFileTypes: acceptFileTypes,
        maxFileSize: maxFileSize,
        messages: messages,
        processfail: safeWrap(function processfailCallback(e, data) {
           var currentFile = data.files[data.index];
           if (data.files.error && currentFile.error) {
               console.error(currentFile.error);
               alert(currentFile.error + ',"' + currentFile.name + '" ' + gettext('removed from upload queue.'));
           }
        }),
        limitConcurrentUploads: 3,
        progressInterval: 50,
        start: safeWrap(function fileuploadStartCallback() {
            _showUploadPopup();
        }),
        done: safeWrap(function fileuploadDoneCallback(e, data) {
            if(!data || !data.result || !data.result.files) {
                return;
            }
            $.each(data.result.files, safeWrap(function resultFilesEachCallback(index, file) {
                $('.files small').text(file.name + ' ' + gettext('upload done.'));
            }));
        }),
        fail: safeWrap(function fileuploadFailCallback(e, data) {
            if(!data || !data.result || !data.result.files) {
                return;
            }
            $.each(data.result.files, safeWrap(function resultFilesEachCallback(index, file) {
                $('.files small').text(file.name + ' ' + gettext('upload fail.'));
                console.error('fileupload.fail:' + file.name);
            }));
        }),
        always: safeWrap(function fileuploadFailCallback(e, data) {
            if(!data || !data.result || !data.result.files) {
                alert(gettext('Network exception, please re-upload the failed one.'));
                return;
            }
            $.each(data.result.files, safeWrap(function resultFilesEachCallback(index, file) {
                console.debug('fileupload.always:' + file.name);
            }));
        }),
        progressall: safeWrap(function fileuploadProgressallCallback(e, data) {
            _updateProgressBar(data.loaded, data.total);
        }),
        stop: safeWrap(function fileuploadStopCallback() {
            _hideUploadPopup();
        })
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
}

function initPictureFileupload() {
    var messages = {
        acceptFileTypes: gettext('Only support GIF/PNG/JPG/JPEG pictures!'),
        maxFileSize: gettext('Picture can not exceed 10MB!')
    };
    _initFileupload('#picture-fileupload',
        '/pic/upload/', /([./])(gif|jpe?g|png)$/i, 20000000, messages);
}

function initVideoFileupload() {
    var messages = {
        acceptFileTypes: gettext('Only support MP4/MOV videos!'),
        maxFileSize: gettext('Video can not exceed 1.5GB!')
    };
    _initFileupload('#video-fileupload',
        '/video/upload/', /([./])(mp4|mov|quicktime)$/i, 1500000000, messages);
}

function initInfiniteScroll(prefix) {
    var $albumMediaData = $('#album-media-data');
    $albumMediaData.infiniteScroll({
        path: safeWrap(function infiniteScrollPath() {
            var pageCount = $albumMediaData.get(0).dataset.pageCount;
            if (!pageCount || this.pageIndex <= pageCount) {
                var albumId = $albumMediaData.get(0).dataset.albumId;
                return '/album/' + albumId + '/more-data/?page=' + this.pageIndex;
            } else {
                return ''
            }
        }),
        checkLastPage: true,
        responseType: 'text',
        scrollThreshold: 120,
        loadOnScroll: true,
        status: '.page-load-status',
        history: false,
        debug: false
    });

    $albumMediaData.on('load.infiniteScroll', safeWrap(function infiniteScrollLoadCallback(event, response, path) {
        // prase response text into JSON data
        var data = '';
        try {
            data = JSON.parse(response);
        } catch(e) {}
        if (data === '') {
            return;
        }
        $albumMediaData.get(0).dataset.pageCount = data.pageCount;
        var itemsHTML = '';
        $.each(data.medias, safeWrap(function mediasEachCallback(index, media) {
            var itemHTML =
                '<div id="media-' + media.id + '" class="col-6 mb-3 px-0">' +
                ' <div class="media-area mx-auto">' +
                '   <div class="edit"><a href="' + media.url + '" type="' + media.contentType + '" {data-poster}>' +
                '       <img src="' + media.thumbnailUrl + '" /></a>' +
                '       <button class="btn btn-sm btn-danger delete" data-id="' + media.id + '" data-delete-url="' + media.deleteUrl + '">' +
                '           <i class="glyphicon glyphicon-trash"></i>' +
                '       </button>' +
                '       <button class="btn btn-sm btn-success cast" data-id="' + media.id + '" data-cast-url="' + media.url + '">' +
                '           <i class="glyphicon glyphicon-collapse-up"></i>' +
                '       </button>' +
                '       {play-button}' +
                '   </div>' +
                ' </div>' +
                '</div>';
            if (media.type === 'video') {
                itemHTML = itemHTML
                    .replace('{data-poster}', ' data-poster="' + media.posterUrl + '"')
                    .replace('{play-button}',
                        '<button class="btn btn-light play">' +
                        '    <i class="glyphicon glyphicon-play"></i>' +
                        '</button>');
            } else {
                itemHTML = itemHTML
                    .replace('{data-poster}', '')
                    .replace('{play-button}', '');
            }
            itemsHTML += itemHTML;
        }));
        // convert to jQuery object
        var $items = $(itemsHTML);
        // append items
        $albumMediaData.infiniteScroll('appendItems', $items);

        resetOp(prefix);
    }));

    $albumMediaData.on('last.infiniteScroll', safeWrap(function infiniteScrollLastCallback(event, error, path) {
        alertMsg('main div.container', gettext('Loading last page!'), 3000);
    }));

    $albumMediaData.on('error.infiniteScroll', safeWrap(function infiniteScrollErrorCallback(event, response, path) {
        alertMsg('main div.container', gettext('No more contents!'), 3000);
    }));

    $albumMediaData.infiniteScroll('loadNextPage');
}

function initBackToTop() {
    $(window).scroll(safeWrap(function windowScrollCallback(event) {
        var $backToTop = $('.back-to-top');
        if (window.pageYOffset >= 400) {
            $backToTop.removeClass('invisible');
        } else {
            $backToTop.addClass('invisible');
        }
    }));
    window.audioPlayer = new Audio();
    var elevator = new Elevator({
        element: document.querySelector('.back-to-top'),
        // audio单例，插件内部实现为2个全局变量，在手机端不能正常工作，故在回调函数中自定义实现。
        // mainAudio: '/static/mp3/elevator.mp3',
        // endAudio: '/static/mp3/ding.mp3',
        duration: 5000,
        startCallback: safeWrap(function elevatorStart() {
            audioPlayer.src = '/static/mp3/elevator.mp3';
            audioPlayer.preload = "true";
            audioPlayer.play()
        }),
        endCallback: safeWrap(function elevatorEnd() {
            audioPlayer.src = '/static/mp3/ding.mp3';
            audioPlayer.preload = "true";
            audioPlayer.play()
        })
    });
}

$(safeWrap(function initDetailJS() {
    var $albumMediaData = $('#album-media-data'),
        $deleteMediaModal = $('#deleteMediaModal'),
        prefix = 'media';

    initPictureFileupload();

    initVideoFileupload();

    // 注册blueimp.Gallery
    initGallery('#album-media-data', 'div[id^="media-"]', true);

    initOpCast(prefix, true);

    castButtonHandler($albumMediaData, prefix);

    initOpEdit(prefix, true);

    initDeleteModal($deleteMediaModal, $albumMediaData,
        'div[id^="media-"] button.delete', prefix, safeWrap(function btnDelMediaClick(id, json) {
            $('#' + prefix + '-' + id).remove();
    }));

    initInfiniteScroll(prefix);
    
    initBackToTop();
}));