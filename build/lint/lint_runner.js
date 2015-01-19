"use strict";

var fs = require("fs");
var jshint = require("jshint").JSHINT;

exports.validateSource = function(sourceCode, options, globals, description) {
    description = description ? description + " " : "";
    var pass = jshint(sourceCode, options, globals);
    if (pass) {
        console.log(description + "ok");
    } else {
        console.log(description + "failed");
        for (var i = 0; i < jshint.errors.length; i++) {
            var error = jshint.errors[i];
            if (!error) continue;
            
            if (error.evidence) {
                console.log(error.line + ": " + error.evidence.trim());
            }
            console.log("   " + error.reason);
        }
    }
    return pass;
};

exports.validateFile = function(filename, options, globals) {
    var sourceCode = fs.readFileSync(filename, "utf8");
    return exports.validateSource(sourceCode, options, globals, filename);
};

exports.validateFileList = function(fileList, options, globals) {
    var pass = true;
    fileList.forEach(function(filename) {
        pass = exports.validateFile(filename, options, globals) && pass;
    });
    return pass;
};
