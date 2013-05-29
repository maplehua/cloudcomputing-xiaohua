 var xmlHttp=null;

$(function () {
    $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
    
        var chart;
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'containerchart',
                type: 'spline',
                marginRight: 10,
                events: {
                    load: function() {
    
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
							  try
  {// Firefox, Opera 8.0+, Safari, IE7
  xmlHttp=new XMLHttpRequest();
  }
catch(e)
  {// Old IE
  try
    {
    xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
  catch(e)
    {
    alert ("Your browser does not support XMLHTTP!");
    return;  
    }
  }
   var url="/api/stat/net";
xmlHttp.open("GET",url,false);
xmlHttp.send(null);
                            var x = (new Date()).getTime(), // current time
                                y = parseInt(xmlHttp.responseText);
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                }
            },
            title: {
                text: '下载流量监控'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: '流量'
                },
       labels: {
        formatter: function() {
            return this.value + ' KB/S';
        }
    },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080',
                
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Download rate',
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
    
                    for (i = -19; i <= 0; i++) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()*1000+3000
                        });
                    }
                    return data;
                })()
            }]
        });
    });
    
});
/////////////////////////////////
////////////////////////////////
//////////////////////////////////
//////////////////////////////////
