var app = (function(jquery, chartjs) {
  var jquery = jquery;
  var chart = chartjs;
  
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
        jquery('#'+data['id']).text(data['value']);
        jquery('#'+data['id']).attr('status', data['status']);
      },
      dataType: "json"}
    );
  }

  var fetchAndPlot = function(set, ctx) {
      jquery.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/api/data",
        data: JSON.stringify({start: Date(2015, 1, 5), end: Date(2015, 12, 31), set: set, team: 1}),
        success: function(data) {
          console.log(data);
          new chart(ctx).Line(data);
        },
        dataType: "json"}
      );
  }

  return {schedule: schedule,
          plotIndexCharts: function(financeCanvas, utilizationCanvas) {
            fetchAndPlot('finance', financeCanvas);
            fetchAndPlot('utilization', utilizationCanvas);
          }}

})($ || {}, Chart.noConflict() || {});
