var app = (function(jquery) {
  var jquery = jquery;

  var schedule = function(e) {
    var source = jquery("#"+e.target.id);
    var status = 'estimated';
    if (source.attr('status') === 'actual') { status = 'removed'; }
    if (source.attr('status') === 'estimated') { status = 'actual'; } 
    jquery.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/api/schedule/iteration-for-engagement",
      data: JSON.stringify({status: status, iteration: source.attr('iteration'), engagement: source.attr('engagement')}),
      success: function(data) {
        console.log(data);
        jquery('#'+data['id']).text(data['value']);
        jquery('#'+data['id']).attr('status', data['status']);
      },
      dataType: "json"}
    );
  }

  return {schedule: schedule};
})($);
