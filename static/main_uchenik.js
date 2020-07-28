$.getJSON('static/graffik.json', function(data_graffik) {
   console.log(data_graffik);



new Chartist.Bar('.chart1', {
  labels: ['алгебра', 'русский'],
  series: [data_graffik],
}, {
  seriesBarDistance: 10,
  reverseData: true,
  horizontalBars: true,
  axisY: {
    offset: 70
  }
});
});