/*!
 * @author: huoyijie
 * @file: my-albums.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

function albumCreateBtnCallback(event) {
    var $form = $('form.needs-validation');
    var $albumNameInput = $('#album-name');
    $albumNameInput.attr('readonly', true);
    var that = $(this);
    that.addClass('disabled');
    that.unbind('click');
    var newAlbumName = $albumNameInput.val();
    var safeWrappedAlbumCreateBtnCallback = safeWrap(arguments.callee);
    if (newAlbumName === '') {
        $form.addClass('was-validated');
        $albumNameInput.attr('readonly', false);
        that.removeClass('disabled');
        that.click(safeWrappedAlbumCreateBtnCallback);
    } else {
        $.ajax({
            url: '/album/create/',
            type: 'POST',
            cache: false,
            data: new FormData($form.get(0)),
            processData: false,
            contentType: false,
            success: safeWrap(function albumCreateSuccessCallback(json) {
                if (json.code === 0) {
                    $('main div.container').append(
                        '<div class="alert" role="alert">' + gettext('Add album successfully.') + '</div>');
                    setTimeout(safeWrap(function closeAlertTimeoutCallback() {
                        $('.alert').alert('close').alert('dispose');
                        setTimeout(safeWrap(function hideModalTimeoutCallback() {
                            $('#createAlbumModal').modal('hide');
                            $albumNameInput.attr('readonly', false);
                            that.removeClass('disabled');
                            that.click(safeWrappedAlbumCreateBtnCallback);
                            window.location.reload();
                        }), 500);
                    }), 1000);
                } else {
                    alert(json);
                    $albumNameInput.attr('readonly', false);
                    that.removeClass('disabled');
                    that.click(safeWrappedAlbumCreateBtnCallback);
                }
            }),
            error: safeWrap(function createAlbumErrorCallback(json) {
                $albumNameInput.attr('readonly', false);
                that.removeClass('disabled');
                that.click(safeWrappedAlbumCreateBtnCallback);
            })
        });
    }
}

function initCreateAlbumModal($createAlbumModal) {
    $createAlbumModal.find('button.submit').click(safeWrap(albumCreateBtnCallback));
    $createAlbumModal.on('hidden.bs.modal', safeWrap(function hiddenModelCallback(event) {
        $('form.needs-validation').removeClass('was-validated');
        $('#album-name').val('');
    }));
}

$(safeWrap(function initMyAlbumsJS() {
    'use strict';
    var targetSelector = '#pagination',
        pagiInfoUrl = '/album/pagi-info/',
        pagiDataUrl = '/album/pagi-data/',
        $paginationData = $('#pagination-data'),
        success = safeWrap(function nextPageClick(json) {
            $('#op-edit')[0].dataset.editState = 'false';
            $('div[id^="album-"]').remove();
            for (var i = 0; i < json.albums.length; i++) {
                var album = json.albums[i];
                $paginationData.append(
                '<div id="album-' + album.id + '" class="col-6 col-md-2 mb-3 px-0">' +
                    '<div class="album-area mx-auto">' +
                    ' <div class="edit">' +
                    '  <a href="/album/detail/' + album.id + '">' +
                    '   <img src="' + album.coverUrl + '" data-src="' + album.holderCoverUrl + '"/>' +
                    '   <div class="album-cover-overlay">' + album.name + '(' + album.mediaCount + ')</div>' +
                    '  </a>' +
                    '  <button class="btn btn-sm btn-danger delete" data-id="' + album.id + '" data-delete-url="' + album.deleteUrl + '">' +
                    '   <i class="glyphicon glyphicon-trash"></i>' +
                    '  </button>' +
                    ' </div>' +
                    '</div>' +
                '</div>'
                );
            }
            Holder.run({
              images: $('div[id^="album-"] img').get()
            });
        }),
        prefix = 'album',
        $createAlbumModal = $('#createAlbumModal'),
        $deleteAlbumModal = $('#deleteAlbumModal');
    initPagination(targetSelector, pagiInfoUrl, pagiDataUrl, success);

    initOpEdit(prefix, false);

    initCreateAlbumModal($createAlbumModal);

    initDeleteModal($deleteAlbumModal, $paginationData,
        'div[id^="album-"] button.delete', prefix, safeWrap(function btnDelAlbumClick(id, json) {
        $('#album-' + id).remove();
        var albumsAfterDel = $paginationData.children().length;
        if (albumsAfterDel <= 0) {
            rebuildPagination(targetSelector, pagiInfoUrl, pagiDataUrl, success);
        }
    }));
}));