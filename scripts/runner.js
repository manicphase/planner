var runner = function(window) {
  var page = require('webpage').create();
  var failures = 0;

  var waitFor = function(pred, callback) {
    var condition = false;
    var intervalId = window.setInterval(function() {
      if (! pred()) {
        console.log("'waitFor()' timeout");
      } else {
        callback();
        window.clearInterval(intervalId);
      }
    }, 100);
  };

  var populateFailures = function() {
    var failed = page.evaluate(function() {
      var el = document.getElementById('qunit-testresult');
      console.log(el.innerText);
      return el.getElementsByClassName('failed')[0].innerHTML;
  };

  var isResultAvailable = function() {
    return page.evaluate(function() {
      var el = document.getElementById('qunit-testresult');
      if (el && el.innerText.match('completed')) { return true; }
      return false;
    }); 
  };

  var main = function() {
    failures = 0;
    page.onConsoleMessage = function(msg) { console.log(msg); };
    page.open(phantom.args[0], function(status) {
      if (status !== 'success') {
        console.log("Unable to access network");
      } else {
        waitFor(run, runSuite);
        phantom.exit(failures);
      }
    });
  };

  return {failures: failures, run: main};
}

if (phantom.args.length === 1) {
  runner.run();
} else {
  runner.failures = -1;
  console.log("Usage: runner.js SuiteUrl");
}
phantom.exit(runner.failures);
