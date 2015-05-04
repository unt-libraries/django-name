(function() {
  'use strict';
})();

var DEFAULT_CHART = 0;

var Statistics = function(options) {
  this.stage = $(options.target);
  this.dataTables = [];

  this.controlWrapper = new google.visualization.ControlWrapper(options.controlConfig);
  this.chartWrapper = new google.visualization.ChartWrapper(options.chartConfig);

  this.dashboard = new google.visualization.Dashboard(this.stage[0]);
  this.dashboard.bind(this.controlWrapper, this.chartWrapper);
  this.piechart = new google.visualization.PieChart(this.stage.find('#piechart')[0]);


  this.stage.on('click', '.chart-nav', $.proxy(this.redrawDashboard, this));

  $.ajax({context: this, url: '/name/stats.json/', success: this.setupDashboard});
};

Statistics.prototype.setupDashboard = function(data) {
  this.dispatch(data);
  this.createPieChart(data); 
  this.drawDashboard(DEFAULT_CHART);
};

Statistics.prototype.drawDashboard = function(chartId) {
  this.dashboard.draw(this.dataTables[chartId]);
};

Statistics.prototype.redrawDashboard = function(e) {
  var chartId = $(e.target).data('chart-id');
  this.drawDashboard(chartId);
};

Statistics.prototype.dispatch = function(data) {
  this.createDataTable(data, 'created', 'total', 'Date Created');
  this.createDataTable(data, 'created', 'total_to_date', 'Total Created');
  this.createDataTable(data, 'modified', 'total', 'Date Modified');
  this.createDataTable(data, 'modified', 'total_to_date', 'Total Modified');
};

Statistics.prototype.createDataTable = function(data, date_type, total_type, label) {
  var dataTable = new google.visualization.DataTable();
  var table = [];

  dataTable.addColumn('date', 'Date');
  dataTable.addColumn('number', label);

  $.each(data[date_type].stats, function(i, v) {
    table.push([new Date(v.month), v[total_type]]);
  });

  dataTable.addRows(table);
  this.dataTables.push(dataTable);
};

Statistics.prototype.createPieChart = function(data) {
  var table = [['type', 'num types']];

  $.each(data.name_type_totals, function(i, v) {
    table.push([i, v]);
  });

  var dataTable = google.visualization.arrayToDataTable(table);

  this.piechart.draw(dataTable, {
    title: 'Name Distribution by Type',
    pieHole: 0.4,
    height: 300,
  });

};

Statistics.create = function() {
  var chartConfig = {
    chartType: 'LineChart',
    containerId: 'chart',
    options: {
      chartArea: {'height': '80%', 'width': '90%'},
      vAxis: {
        gridlines: {count: 10},
      },
      legend: {'position': 'none'}
    }
  };

  var controlConfig = {
    controlType: 'ChartRangeFilter',
    containerId: 'control',
    options: {
      filterColumnIndex: 0,
      ui: {
        chartType: 'LineChart',
        chartOptions: {
          chartArea: {'width': '90%', height: '50%'},
        },
        minRangeSize: 2678000000, // Milliseconds in 1 month (31 days).
      },
    },
  };

  return new Statistics({
    controlConfig: controlConfig,
    chartConfig: chartConfig,
    target: '#dashboard'
  });
};

google.load('visualization', '1.1', {packages: ['corechart', 'controls']});
google.setOnLoadCallback(Statistics.create);
