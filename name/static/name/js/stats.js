(function() {
  'use strict';
})();

var Statistics = function() {
  this.chartConfig = {
    chartType: 'LineChart',
    containerId: 'chart',
    options: {
      chartArea: {'height': '80%', 'width': '90%'},
      hAxis: {
        slantedText: false,
      },
      vAxis: {
        gridlines: {count: 10},
        textStyle: {color: 'black', fontName: 'arial', fontSize: 11}
      },
      legend: {'position': 'none'}
    }
  };

  this.control = {
    controlType: 'ChartRangeFilter',
    containerId: 'control',
    options: {
      filterColumnIndex: 0,
      ui: {
        chartType: 'LineChart',
        chartOptions: {
          chartArea: {'width': '90%'},
          hAxis: {'baselineColor': 'none'},
        },
        chartView: {
          columns: [0, 1],
        },
        minRangeSize: 86400000,
      },
    },
    state: {
      range: {start: new Date(2004, 11, 1), end: new Date()},
    }
  };

  this.dataTables = [];

  this.controlWrapper = new google.visualization.ControlWrapper(this.control);
  this.chartWrapper = new google.visualization.ChartWrapper(this.chartConfig);
  this.dashboard = new google.visualization.Dashboard(document.getElementById('dashboard'));

  this.data = $.ajax({context: this, async: false, url: '/name/stats.json/'}).responseJSON;
  this.drawDashboard();
};

Statistics.prototype.drawDashboard = function() {
  $('.chart-nav').on('click', $.proxy(function(e){
    var chartId = $(e.target).data('chart-id');
    this.chartListener(chartId);
  }, this));

  this.dispatch();
  this.dashboard.bind(this.controlWrapper, this.chartWrapper);
  this.chartListener(0);
};

Statistics.prototype.chartListener = function(chartId) {
  this.dashboard.draw(this.dataTables[chartId]);
};

Statistics.prototype.dispatch = function() {
  this.createDataTable('created', 'total', 'Date Created');
  this.createDataTable('created', 'total_to_date', 'Total Created');
  this.createDataTable('modified', 'total', 'Date Modified');
  this.createDataTable('modified', 'total_to_date', 'Total Modified');
};

Statistics.prototype.createDataTable = function(date_type, total_type, label) {
  var dataTable = new google.visualization.DataTable();
  var table = [];

  dataTable.addColumn('date', 'Date');
  dataTable.addColumn('number', label);

  $.each(this.data[date_type].stats, function(i, v) {
    table.push([new Date(v.month), v[total_type]]);
  });

  dataTable.addRows(table);
  this.dataTables.push(dataTable);
};

Statistics.create = function() {
  return new Statistics();
};

google.load('visualization', '1.1', {packages: ['corechart', 'controls']});
google.setOnLoadCallback(Statistics.create);

