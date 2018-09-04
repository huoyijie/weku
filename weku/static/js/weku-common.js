/*!
 * @author: huoyijie
 * @file: weku-common.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

function initGallery(delegateSelector, targetSelector, includeVideo) {
    var $delegateObj = $(delegateSelector);
    $delegateObj.on('click', targetSelector + ' a', safeWrap(function callGallery1(event) {
        event = event || window.event;
        event.preventDefault();
        var target = event.target || event.srcElement,
            link = target.src ? target.parentNode : target,
            options = {index: link, event: event, slideshowInterval: 2500},
            links = $delegateObj.find('a');
        blueimp.Gallery(links, options);
    }));
    if(includeVideo) {
        $delegateObj.on('click', targetSelector + ' button.play', safeWrap(function callGallery2(event) {
            event = event || window.event;
            event.preventDefault();
            var target = event.target || event.srcElement,
                button = target.tagName.toLowerCase() === 'button'
                    ? target : target.parentNode,
                link = $(button).siblings('a').get(0),
                options = {index: link, event: event, slideshowInterval: 2500},
                links = $delegateObj.find('a');
            blueimp.Gallery(links, options);
        }));
    }
}

function _initPagination(targetSelector, totalPages, startPage, pagiDataUrl, success) {
    window.pagObj = $(targetSelector).twbsPagination({
        totalPages: totalPages,
        startPage: startPage,
        visiblePages: 1,
        first: gettext('First'),
        last: gettext('Last'),
        prev: gettext('Previous'),
        next: gettext('Next'),
        onPageClick: safeWrap(function onPageClick(event, page) {
            window.location.hash = '#page' + page;
            $.ajax({
                url: pagiDataUrl + '?page=' + page,
                contentType: 'application/json',
                type: 'get',
                cache: false,
                dataType: 'json',
                success: safeWrap(success)
            });
        })
    });
}

function initPagination(targetSelector, pagiInfoUrl, pagiDataUrl, success) {
    $.get(pagiInfoUrl, {}, safeWrap(function initPaginationCallback(data) {
        var totalPages = data.page_count;
        if (totalPages > 0) {
            var startPage = 1;
            var hashStr = window.location.hash,
                urlHasPage =
                    hashStr &&
                    hashStr.indexOf('#page') === 0 &&
                    hashStr.length > 5;
            if (urlHasPage) {
                startPage = parseInt(window.location.hash.substring(5));
            }
            _initPagination(targetSelector, totalPages, startPage, pagiDataUrl, success);
        }
    }));
}

function rebuildPagination(targetSelector, pagiInfoUrl, pagiDataUrl, success) {
    $.ajax({
        url: pagiInfoUrl,
        contentType: 'application/json',
        type: 'get',
        cache: false,
        dataType: 'json',
        success: safeWrap(function rebuildPaginationCallback(json) {
            var totalPages = json.page_count;
            var $pagination = $(targetSelector);
            var startPage = $pagination.twbsPagination('getCurrentPage');
            if (startPage === undefined) {
                startPage = 1;
            }
            if (startPage > totalPages) {
                startPage = totalPages;
            }
            $pagination.twbsPagination('destroy');
            if (totalPages > 0) {
                _initPagination(targetSelector, totalPages, startPage, pagiDataUrl, success);
            }
        })
    });
}

function initOpCast(prefix, withEdit) {
    $('#op-cast').on('click', safeWrap(function btnOpCastClick() {
        var castState = this.dataset.castState,
            $target = $('div[id^="' + prefix + '-"]'),
            $castButton = $target.find('button.cast');
        if(withEdit) {
            var $opEdit = $('#op-edit'),
                editState = $opEdit[0].dataset.editState;
            if (editState === 'true') {
                $opEdit[0].dataset.editState = 'false';
                $target.find('button.delete').css('visibility', 'hidden');
            }
        }
        if (castState === 'false') {
            this.dataset.castState = 'true';
            $target.removeClass('mb-3').addClass('mb-5');
            $castButton.css('visibility', 'visible');
        } else {
            this.dataset.castState = 'false';
            $target.removeClass('mb-5').addClass('mb-3');
            $castButton.css('visibility', 'hidden');
        }
    }));
}

function initOpEdit(prefix, withCast) {
    $('#op-edit').on('click', safeWrap(function btnOpEditClick() {
        var editState = this.dataset.editState,
            $target = $('div[id^="' + prefix + '-"]'),
            $editButton = $target.find('button.delete');
        if(withCast) {
            var $opCast = $('#op-cast'),
                castState = $opCast[0].dataset.castState;
            if (castState === 'true') {
                $opCast[0].dataset.castState = 'false';
                $target.find('button.cast').css('visibility', 'hidden');
            }
        }
        if (editState === 'false') {
            this.dataset.editState = 'true';
            $target.removeClass('mb-3').addClass('mb-5');
            $editButton.css('visibility', 'visible');
        } else {
            this.dataset.editState = 'false';
            $target.removeClass('mb-5').addClass('mb-3');
            $editButton.css('visibility', 'hidden');
        }
    }));
}

function resetOp(prefix) {
    var $target = $('div[id^="' + prefix + '-"]'),
        $castButton = $target.find('button.cast'),
        $editButton = $target.find('button.delete');
    $target.removeClass('mb-5').addClass('mb-3');
    $castButton.css('visibility', 'hidden');
    $editButton.css('visibility', 'hidden');
    $('#op-cast')[0].dataset.castState = 'false';
    $('#op-edit')[0].dataset.editState = 'false';
}

function pagiDataDelButtonHandler($paginationData, prefix, success) {
    $paginationData.on('click', 'div[id^="' + prefix + '-"] button.delete', safeWrap(function btnDelClick() {
        var url = this.dataset.deleteUrl;
        var id = this.dataset.id;
        $.ajax({
            url: url,
            contentType: 'application/json',
            type: 'delete',
            cache: false,
            dataType: 'json',
            success: safeWrap(success)
        });
    }));
}

function alertMsg(appendToSelector, msg, timeout) {
    $(appendToSelector).append(
        '<div class="alert h5 text-center" role="alert">' +
            msg +
        '</div>');
    setTimeout(safeWrap(function closeAlertTimeoutCallback() {
        $('.alert').alert('close').alert('dispose');
    }), timeout);
}

function alertMsg2(appendToSelector, msg, timeout, position) {
    var midPosition = (Math.ceil(window.innerHeight * 0.5) + window.pageYOffset) + 'px';
    if (!position || position === 'middle') {
        position =  midPosition;
    } else if(position === 'top') {
        position = (Math.ceil(window.innerHeight * 0.1) + window.pageYOffset) + 'px';
    } else if(position === 'bottom') {
        position = (Math.ceil(window.innerHeight * 0.9) + window.pageYOffset) + 'px';
    } else {
        position =  midPosition;
    }
    $(appendToSelector).append(
        '<div class="alert h5 text-center" role="alert">' +
            msg +
        '</div>');
    var $alert = $('.alert').css('top', position);
    setTimeout(safeWrap(function closeAlertTimeoutCallback() {
        $alert.alert('close').alert('dispose');
    }), timeout);
}

function _dlnacast(castUrl, device) {
    var encodeCastUrl = encodeURI(window.location.origin + castUrl);
    $.get('/dlnacast/cast/',
        {
            castUrl: encodeCastUrl,
            device: device
        },
        safeWrap(function dlnacastAlert(data) {
            var alert_msg = '';
            if (data.code === 0) {
                alert_msg = gettext('DLNA cast successfully.');
            } else {
                alert_msg = data.msg;
            }
            alertMsg('main div.container', alert_msg, 2000);
    }));
}

function castButtonHandler($paginationData, prefix) {
    $paginationData.on('click', 'div[id^="' + prefix + '-"] button.cast', safeWrap(function btnCastClick() {
        _dlnacast(this.dataset.castUrl, '');
    }));
}

function initDeleteModal($deleteModal, $delegateObj, targetSelector, prefix, callback) {
    $deleteModal.find('button.submit').click(safeWrap(function btnSubmitClick(event) {
       $deleteModal
            .data('closeBy', 'submit')
            .modal('hide');
    }));
    $delegateObj.on('click', targetSelector, safeWrap(function btnDelClick() {
        var id = this.dataset.id,
            url = this.dataset.deleteUrl;
        $deleteModal
            .one('hide.bs.modal', safeWrap(function hideModalCallback(event) {
                if($(this).data('closeBy') === 'submit') {
                    $.ajax({
                        url: url,
                        contentType: 'application/json',
                        type: 'delete',
                        cache: false,
                        dataType: 'json',
                        success: safeWrap(function delSuccessCallback(json) {
                            if(callback) {
                                callback(id, json);
                            }
                        })
                    });
                    $(this).data('closeBy', '');
                }
            }))
            .modal('show');
   }));
}