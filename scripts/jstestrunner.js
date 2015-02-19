/*global document, require, phantom, window, console*/
(function () {
    'use strict';
    var page = require('webpage').create(),
        failures = null,
        threeSeconds = 3001,
        url = 'test/tests.html',
        results = [];

    var concluded = function (cond, start, timeout) {
        return new Date().getTime() - start >= timeout || cond;
    };

    var waitFor = function (pred, callback, timeout, next) {
        var start = new Date().getTime();
        var cond = false;
        var  interval = window.setInterval(function () {
            if (concluded(cond, start, timeout)) {
                window.clearInterval(interval);
                if (cond) {
                    callback();
                } else {
                    failures = -1;
                }
                next();
            } else {
                cond = pred();
            }
        }, 100);
    };

    var populateFailures = function () {
        failures = 0;
        page.evaluate(function () {
            var i,
                result,
                resultHtml,
                elements = document.getElementById('quint-tests').childNodes;
            for (i = 0; i < elements.length; i = i + 1) {
                resultHtml = elements[i];
                result = {};
                result.name = resultHtml.getElementsByClassName('test-name')[0].textContent;
                result.msg = resultHtml.getElementsByClassName('test-message')[0].textContent;
                result.time = resultHtml.getElementsByClassName('runtime')[0].textContent;
                result.diff = resultHtml.getElementsByClassName('test-diff')[0].textContent;
                result.source = resultHtml.getElementsByClassName('test-source')[0].textContent;
                result.status = resultHtml.className;
                if (resultHtml.className === "fail") {
                    failures = failures + 1;
                }
                results.push(result);
            }
        });
    };

    var isResultAvailable = function () {
        return page.evaluate(function () {
            var el = document.getElementById('qunit-testresult') || '';
            return el.textContent.indexOf('completed') > -1;
        });
    };

    var exit = function () {
        if (failures === -1) {
            console.log("ERROR: TIMEOUT");
        } else {
            var i;
            for (i = 0; i < results.length; i = i + 1) {
                var result = results[i];
                console.log('[' + result.time + '] ' + result.name + ': ' + result.msg + ' -> ' + result.status + '...\n' + result.diff + '\n\t\t' + result.source);
            }
            if (failures === 0) {
                console.log("PASSED");
            } else {
                console.log("FAILED");
            }
        }
        phantom.exit(failures);
    };

    page.open(url, function () {
        waitFor(isResultAvailable, populateFailures, threeSeconds, exit);
    });
}());
