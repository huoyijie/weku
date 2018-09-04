/*!
 * @author: huoyijie
 * @file: csrf.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

// modify jquery ajax to add csrtoken when doing "local" requests
$(document).ajaxSend(Raven.wrap(function(event, xhr, options) {
    if (!(/^http:.*/.test(options.url) || /^https:.*/.test(options.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    }
}));