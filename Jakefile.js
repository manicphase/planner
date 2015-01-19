(function() {
  "use strict";

  var NODE_VERSION = "v0.10.";
  var syscmd = require('procstreams');

  desc("Deploy and run locally");
  task("deploylocal", ["default", "minify"]);

  desc("Build and Test");
  task("default", ["testpy", "testjs"]);

  desc("Run Python Tests");
  task("testpy", [], function() {
    syscmd("python -m unittest discover -s test -p _test_*.py").data(function(err, stdout, stderr) {
      if (err) {
        console.log(stdout.toString());
        console.log(stderr.toString());
        fail("Python Unittest Failure.");
      }
      complete();
    });
  }, {async:true});

  desc("Run Javascript Tests");
  task("testjs", ["lintjs"]);

  desc("Lint Javascript");
  task("lintjs", ["jsdevdeps"], function() {
    var lint = require("./build/lint/lint_runner.js");

    var srcFiles = new jake.FileList();
    srcFiles.include("plannerjs/*.js");

    var options = nodeLintOptions();

    var passed = lint.validateFileList(srcFiles.toArray(), options, {});
    if (! passed) fail("Javascript Linting Failed.");
  });

  desc("Setup Javascript Development Dependencies");
  task("jsdevdeps", ["node"], function() {
    syscmd("npm install --dev").data(function(err, stdout, stderr) {
      if (err) fail("npm failed to install dev dependencies for javascript.");
      complete();
    });
  }, {async:true});

  desc("Check for Node compatibility");
  task("node", [], function() {
    syscmd("node --version").data(function(err, stdout, stderr) {
      if (err) fail("No Node available."); 
      if (stdout.toString().trim().indexOf(NODE_VERSION) !== 0) fail("Incompatible node.js version found.");
      complete();
    });
  }, {async:true});

  desc("Minify and deploy Javascript");
  task("minify", [], function() {
    new compressor.minify({
      type: 'gcc',
      fileIn: ['plannerjs/main.js'],
      fileOut: 'planner/static/main.js',
      callback: function(err, min) {
        if (err) fail(err);
        complete();
      }
    });
  });

  function nodeLintOptions() {
    return {bitwise:true,
            curly:false,
            eqeqeq:true,
            forin:true,
            immed:true,
            latedef:true,
            newcap:true,
            noarg:true,
            noempty:true,
            nonew:true,
            regexp:true,
            undef:true,
            strict:true,
            trailing:true,
            node:false}
  }
}());
