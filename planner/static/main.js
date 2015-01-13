var app = (function(jquery, graph) {
  var jquery = jquery;
  var graph = graph;

  var start = Date();
  start.setFullYear(2015, 0, 5);
  var end = Date();
  end.setFullYear(2015, 11, 31);

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

  var drawCost = function(target) {
    jquery.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/api/data",
      data: JSON.stringify({start: start, end: end, set: "cost", team:1}),
      success: function(data) {
        //TODO: Make it so
        graph(target.getContext("2d")).Line(data, options);
      },
      dataType: "json"}
    );
  }

  var drawRevenue = function(target) {
    jquery.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/api/data",
      data: JSON.stringify({start: start, end: end, set: "revenue", team:1}),
      success: function(data) {
        //TODO: Make it so
        graph(target.getContext("2d")).Line(data, options);
      },
      dataType: "json"}
    );
  }

  var drawUtilization = function(target) {
    jquery.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/api/data",
      data: JSON.stringify({start: start, end: end, set: "utilization", team:1}),
      success: function(data) {
        graph(target.getContext("2d")).Line(data, options);
      },
      dataType: "json"}
    );
  }

  return {schedule: schedule,
          revenue: drawRevenue,
          utilization: drawUtilization};
})($, Chart);
