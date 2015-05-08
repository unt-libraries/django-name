'use strict';

var DEFAULT_CHART = 0;

/** 
 * Creates a series of graphs to visually represent
 * Name data.
 */
var Statistics = function(options) {
  this.stage = $(options.stage);
  this.dataTables = [];

  // Configure the Dashboard.
  this.controlWrapper = new google.visualization.ControlWrapper(options.controlConfig);
  this.chartWrapper = new google.visualization.ChartWrapper(options.chartConfig);

  this.dashboard = new google.visualization.Dashboard(this.stage[0]);
  this.dashboard.bind(this.controlWrapper, this.chartWrapper);

  // Configure the Pie Chart.
  this.piechart = new google.visualization.PieChart(this.stage.find('#piechart')[0]);

  // Bind the click event on the .chart-nav buttons to trigger the
  // redrawDashboard method.
  this.stage.on('click', '.chart-nav', $.proxy(this.redrawDashboard, this));

  // Get the Name data.
  $.ajax({
    context: this,
    url: this.stage.find('form').attr('action'),
    success: this.setupDashboard
  });
};

/**
 * Setup the Dashboard
 *
 * Creates the DataTables and draws the Dashboard.
 */
Statistics.prototype.setupDashboard = function(data) {
  this.createDataTables(data);
  this.createPieChart(data); 
  this.drawDashboard(DEFAULT_CHART);
};

/**
 * Draw the dashboard.
 * 
 * chartId is the index of the array this.dataTables that 
 * is to be displayed.
 */
Statistics.prototype.drawDashboard = function(chartId) {
  this.dashboard.draw(this.dataTables[chartId]);
};

/**
 * Event handler to redraw the dashboard to display
 * the designated datatable.
 */
Statistics.prototype.redrawDashboard = function(e) {
  var chartId = $(e.target).data('chart-id');
  this.drawDashboard(chartId);
};

/** 
 * Create DataTables for date_created and last_modifed data.
 */
Statistics.prototype.createDataTables = function(data) {
  this.convertToDataTable(data, 'created', 'total', 'Date Created');
  this.convertToDataTable(data, 'created', 'total_to_date', 'Total Created');
  this.convertToDataTable(data, 'modified', 'total', 'Date Modified');
  this.convertToDataTable(data, 'modified', 'total_to_date', 'Total Modified');
};

/**
 * Convert a JSON object to an array for use
 * as a DataTable.
 */
Statistics.prototype.convertToDataTable = function(data, date_type, total_type, label) {
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

/**
 * Create Pie Chart
 */
Statistics.prototype.createPieChart = function(data) {
  var dataTable = google.visualization.arrayToDataTable([
    ['type', 'num types'],
    ['Personal', data.name_type_totals.personal],
    ['Organization', data.name_type_totals.organization],
    ['Building', data.name_type_totals.building],
    ['Event', data.name_type_totals.event],
    ['Software', data.name_type_totals.software],
  ]);

  this.piechart.draw(dataTable, {
    title: 'Name Distribution by Type',
    pieHole: 0.4,
    height: 300,
  });
};

/**
 * Create
 *
 * Class method to create a new Statistics instance. 
 * Useful as an event handler.
 */
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
    stage: '#dashboard',
  });
};

// Get the visualization packages and set the callback.
google.load('visualization', '1.1', {packages: ['corechart', 'controls']});
google.setOnLoadCallback(Statistics.create);
