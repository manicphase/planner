/*global document, require, phantom, window, console*/
(function () {
    'use strict';
    var page = require('webpage').create(),
        threeSeconds = 3001,
        url = 'test/tests.html',
        report;

    var concluded = function (cond, start, timeout) {
        return new Date().getTime() - start >= timeout || cond;
    };

    var waitFor = function (pred, callback, timeout, next) {
        var start = new Date().getTime(),
            cond = false;
        var  interval = window.setInterval(function () {
            if (concluded(cond, start, timeout)) {
                window.clearInterval(interval);
                if (cond) {
                    next(callback());
                }
                next();
            } else {
                cond = pred();
            }
        }, 100);
    };

    var populateFailures = function () {
        report = page.evaluate(function () {
            var tests = document.getElementById('qunit-tests').childNodes;
            var results = [];
            var result;
            var resultHtml;
            var failures = 0;
            var i;
            for (i = 0; i < tests.length; i = i + 1) {
                if (tests[i].className === 'fail') {
                    failures = failures + 1;
                }
                resultHtml = tests[i];
                console.log(resultHtml);
                result = {};
                result.status = resultHtml.className;
                result.name = resultHtml.getElementsByClassName('test-name')[0].textContent;
                result.time = resultHtml.getElementsByClassName('runtime')[0].textContent;
                result.msg = '';
                result.diff = '';
                result.source = '';
                if (result.status === 'fail') {
                    result.msg = resultHtml.getElementsByClassName('test-message')[0].textContent;
                    result.source = resultHtml.getElementsByClassName('test-source')[0].textContent;
                    if (result.msg.indexOf('Died') !== 0) {
                        result.diff = resultHtml.getElementsByClassName('test-diff')[0].textContent;
                    } else {
                        result.status = 'error';
                    }
                }
                results.push(result);
            }
            return {'failures': failures, 'results': results};
        });
    };

    var isResultAvailable = function () {
        return page.evaluate(function () {
            var el = document.getElementById('qunit-testresult') || '';
            return el.textContent.indexOf('completed') > -1;
        });
    };

    var exit = function () {
        if (report === null) {
            console.log("ERROR");
            phantom.exit(1);
        } else {
            var i,
                results = report.results,
                result;
            for (i = 0; i < results.length; i = i + 1) {
                result = results[i];
                console.log(result.status.toUpperCase() + ' [' + result.time + '] ' + result.name + '\n');
                if (result.status === 'fail') {
                    console.log(result.msg + '\n' + result.diff + '\n' + result.source + '\n');
                } else if (result.status === 'error') {
                    console.log(result.msg + '\n' + result.source + '\n');
                }
            }
            if (report.failures === 0) {
                console.log("PASSED");
            } else {
                console.log("FAILED");
            }
        }
        phantom.exit(report.failures);
    };

    page.onConsoleMessage = function (msg) {
        console.log("BROWSER CONSOLE: " + msg);
    };

    page.onError = function (msg, trace) {
        console.log("BROWSER CONSOLE ERROR: " + msg);
    };

    page.onResourceError = function (metadata) {
        console.log("BROWSER CONSOLE RESOURCE ERROR: " + metadata.errorString);
    };

    page.open(url, function () {
        waitFor(isResultAvailable, populateFailures, threeSeconds, exit);
    });
}());
