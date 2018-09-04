/*!
 * @author: huoyijie
 * @file: base.js
 * @time: 2018/08/29
 *
 * @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
 * @license: GPL v3, see LICENSE for more details.
 */

function _checkFuncWrapped(func) {
    // We don't wanna wrap it twice!
    try {
      if (func.__func_wrapped__) {
        return func;
      }

      // If this has already been wrapped in the past, return that
      if (func.__func_wrapper__) {
        return func.__func_wrapper__;
      }
    } catch (e) {
      // Just accessing custom props in some Selenium environments
      // can cause a "Permission denied" exception (see raven-js#495).
      // Bail on wrapping and return the function as-is (defers to window.onerror).
      return func;
    }
    return null;
}

function _checkWrapped(func, wrappedProperty, wrapperProperty) {
    // We don't wanna wrap it twice!
    try {
      if (func[wrappedProperty]) {
        return func;
      }

      // If this has already been wrapped in the past, return that
      if (func[wrapperProperty]) {
        return func[wrapperProperty];
      }
    } catch (e) {
      // Just accessing custom props in some Selenium environments
      // can cause a "Permission denied" exception (see raven-js#495).
      // Bail on wrapping and return the function as-is (defers to window.onerror).
      return func;
    }
    return null;
}

function _funcWrap(func, options, before, after) {
    if (!$.isFunction(func)) {
        throw new TypeError('func is not a function!');
    }

    if (!options || !$.isPlainObject(options)) {
        throw new TypeError('options is not a plain object!');
    }

    var checkResult = _checkWrapped(func, '__func_wrapped__', '__func_wrapper__');
    if (checkResult && $.isFunction(checkResult)) {
        return checkResult;
    }

    function wrapped() {
        var args = [];
        args.push(options);
        for (var key in arguments) {
            args.push(arguments[key]);
        }
        if ($.isFunction(before)) {
            before.apply(this, args);
        }
        var ret = func.apply(this, arguments);
        if ($.isFunction(after)) {
            after.apply(this, args);
        }
        return ret;
    }

    // copy over properties of the old function
    for (var property in func) {
      if (hasKey(func, property)) {
        wrapped[property] = func[property];
      }
    }
    wrapped.prototype = func.prototype;

    func.__func_wrapper__ = wrapped;
    // Signal that this function has been wrapped/filled already
    // for both debugging and to prevent it to being wrapped/filled twice
    wrapped.__func_wrapped__ = true;
    wrapped.__orig__ = func;

    return wrapped;
}

function _metricsWrap(func, metricEventName) {
    var metric = new Metric(metricEventName);
    return _funcWrap(func, {
            metric: metric
        }, function (options) {
            options.metric.start();
        }, function (options) {
            options.metric.end();
            console.debug(
                'appmetrics',
                options.metric.name,
                options.metric.duration,
                'ms');
        });
}

function safeWrap(func, options) {
    if (!$.isFunction(func)) {
        throw new TypeError('func is not a function!');
    }

    var checkResult = _checkWrapped(func, '__func_wrapped__', '__func_wrapper__');
    if (checkResult && $.isFunction(checkResult)) {
        return checkResult;
    }

    checkResult = _checkWrapped(func, '__raven__', '__raven_wrapper__');
    if (checkResult && $.isFunction(checkResult)) {
        return checkResult;
    }

    if (!options || !$.isPlainObject(options)) {
        options = {disableMetric: true};
    }

    var wrapped = func;
    if (options.metricEventName) {
        wrapped = _metricsWrap(func, options.metricEventName);
    } else if(!options.disableMetric) {
        var eventName = func.toString();
        if (func.name) {
            eventName = func.name;
        }
        wrapped = _metricsWrap(func, eventName);
    }

    // fixme 如何正确配置了Raven，此处可以打开开关
    var ravenConfigured = false;
    if (ravenConfigured && !options.disableRaven) {
        wrapped = Raven.wrap(wrapped);
    }

    return wrapped;
}

function debug_entry(selector, callback) {
    var count = 0,
        entry = document.querySelector(selector);
    if(entry) {
        entry.addEventListener('click', function () {
            count++;
            if (count > 5) {
                count = 0;
                callback();
            }
        })
    }
}

$(function () {

    /*
     * fixme 打开注释并正确配置Raven开启Sentry JS Error Report(需确保已正确安装Sentry)
     * Raven.config('http://eb6d5848c44145238f7e1103348c40dc@192.168.31.53:9000/3', {
     *  release: '1.0.0'
     * }).install();
     */

    AlloyLever.config({
        cdn: '/static/js/vconsole.min.js',  //vconsole的url地址
        reportUrl: "/index/",  //错误上报地址
        reportPrefix: 'weku',    //错误上报msg前缀，一般用于标识业务类型
        reportKey: 'msg',        //错误上报msg前缀的key，用户上报系统接收存储msg
        otherReport: {              //需要上报的其他信息
            key: 'value'
        }/*,
        entry: '#entry1'
                 //请点击这个DOM元素6次召唤vConsole。//你可以通过AlloyLever.entry('#entry2')设置多个机关入口召唤神龙*/
    });

    debug_entry('#entry1', function () {
        $.get('/debug/', {'switch': 'toggle'}, safeWrap(function debugEntryTaggle(json) {
            var href = window.location.href;
            if (json.isDebug) {
                if (window.location.search)
                    if (href.charAt(href.length - 1) === '&') {
                        href += 'vconsole=hide';
                    } else {
                        href += '&vconsole=hide';
                    }
                else {
                    if (href.charAt(href.length - 1) === '?') {
                        href += 'vconsole=hide';
                    } else {
                        href += '?vconsole=hide';
                    }
                }
            } else {
                href = href.replace('vconsole=hide', '');
            }
            window.location.href = href;
        }));
    });

});