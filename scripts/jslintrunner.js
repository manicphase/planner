/*global phantom, JSLINT, require, console*/
(function () {
    'use strict';

    var fs = require('fs'),
        failed = 0,
        i,
        j,
        lintConfig = {
            vars: true
        };
    phantom.injectJs('scripts/jslint.js');
    for (i = 0; i < phantom.args.length; i = i + 1) {
        var filename = phantom.args[i];
        JSLINT(fs.read(filename), lintConfig);
        if (JSLINT.errors.length !== 0) {
            failed = failed + 1;
            console.log(filename + " FAILED");
            for (j = 0; j < JSLINT.errors.length; j = j + 1) {
                var error = JSLINT.errors[j];
                if (error !== null) {
                    console.log(filename + ":" + error.line + " [" + error.character + "] " + error.reason);
                }
            }
        } else {
            console.log(filename + " OK");
        }
    }
    phantom.exit(failed);
}());
