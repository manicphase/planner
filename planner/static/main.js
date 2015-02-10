/* global $, Chart */

var app = (function(jquery, Chartjs) {
  "use strict";

  var ajax = function(path, data, callback) {
    jquery.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: JSON.stringify(data),
      success: callback,
      dataType: "json"
    });
  };

  var flashHtml = function(message, cssClass) {
    return '<div id="flashes" class="container alert '+cssClass+'><button type="button" data-dismiss="alert" class="close"><span aria-hidden="true">x</span><span class="sr-only">Close</span></button><p>'+message+'</p></div>'
  };

  var newClientFormHtml = function() {
    <form entity="Client">
      <div class="form-group" field="name">
        <label class="control-label">Name</label>
        <input class="form-control" type="text" value>
      </div>
      <button class="btn btn-default" onclick=formSubmitter(this)>Submit</button>
    </form>
  };

  var markAllErrors = function(data) {
    for (error in data) markError(error);
  };

  var markError = function(data) {
    jquery('#'+data.id).addClass('has-error');
    jquery('#'+data.id).append('<p> class="help-block">'+data.message+'</p>');
  };

  var unmarkAllErrors = function() {
    jquery('div.has-error p').remove();
    jquery('div.has-error').removeClass('has-error');
  };

  var flashSuccessHandler = function(data) {
    unmarkAllErrors();
    jquery('#flashes').remove();
    jquery('#header').prepend(flashHtml(data.message, 'success'));
  };

  var flashErrorHandler = function(data) {
    unmarkAllErrors();
    jquery('#flashes').remove();
    jquery('#header').prepend(flashHtml(data.message, 'danger'));
    markAllErrors();
  };

  var formSubmitter = function(el) {
    var data = {};
    data.entity = el.parent().attr('entity');
    for (del in el.siblings()) {
      data[del.attr('field')] = del.children('input').attr('value');
    }
    ajax(el.attr(url), data, el.attr(callback));
  };

  var newClientForm = function(el) {
    el.append(newClientFormHtml());
  };

  return {}
})($ || {}, Chart.noConflict() || {});
