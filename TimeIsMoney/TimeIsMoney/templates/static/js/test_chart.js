function hourlyChart(hourly_data_market_price, hourly_data_quantity) {
  console.log(hourly_data_quantity.toString());
  Highcharts.chart('container', {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: 'USD to EUR exchange rate over time'
    },
    subtitle: {
      text: document.ontouchstart === undefined ?
        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
    },
    xAxis: {
      type: 'datetime',
      labels: {
        format: '{value:%b-%e}'
      },
      tickInterval: 24 * 3600 * 1000,
    },
    yAxis: [{
      title: {
        text: 'Quantity'
      },
      min: 0,
      //gridLineWidth: 1,
      allowDecimals: false,
      opposite: true
    }, {
      gridLineWidth: 0,
      title: {
        text: 'Market price'
      },
      min: 0
    }],
    tooltip: {
      shared: true,
      crosshairs: [true]
    },
    legend: {
      enabled: true
    },
    plotOptions: {
      area: {
        fillColor: {
          linearGradient: {
            x1: 0,
            y1: 0,
            x2: 0,
            y2: 1
          },
          stops: [
            [0, Highcharts.getOptions().colors[0]],
            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
          ]
        },
        marker: {
          radius: 0
        },
        lineWidth: 1,
        states: {
          hover: {
            lineWidth: 1
          }
        },
        threshold: null
      },
      line: {
        marker: {
          radius: 0
        }
      }
    },

    series: [{
      type: 'area',
      name: 'Market price',
      yAxis: 1,
      data: hourly_data_market_price
    },{
      type: 'line',
      name: 'Quantity',
      yAxis: 0,
      data: hourly_data_quantity
    }]
  });
}