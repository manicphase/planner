/*global $, Chart, console*/

var populate_revenue_graph = function () {
    "use strict";
    var finances_data_url = "http://127.0.0.1:5000/api/schedule/engagement_iterations";
    $.getJSON(finances_data_url, {})
        .done(function (data) {
            var revenues = data.revenue;
            var costs = data.cost;
            var ticks = [];
            var i = 0;
            // set ticks manually, otherwise flot tries to help
            for (i = 0; i < costs.length; i = i + 1) {
                ticks.push(costs[i][0]);
            }
            var datas = [
                {
                    label: "revenues",
                    data: revenues
                },
                {
                    label: "costs",
                    data: costs
                }
            ];
            var options = {
                xaxis: {
                    mode: 'time',
                    timeformat: "%Y-%m-%d",
                    rotateTicks: 0,
                    ticks: ticks
                }
            };
            $.plot("#finance", datas, options);
        })
        .fail(function () {
            console.log("failed to get json data");
        });
};
