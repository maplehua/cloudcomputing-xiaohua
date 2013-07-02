$(document).ready(function() {
				 new Highcharts.Chart({
					chart: {
						renderTo: 'abc',
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false
					},
					title: {
						text: ' '
					},
					tooltip: {
						formatter: function() {
							return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
						}
					},
					plotOptions: {
						pie: {
							allowPointSelect: true,
							cursor: 'pointer',
							dataLabels: {
								enabled: true,
								color: '#000000',
								connectorColor: '#000000',
								formatter: function() {
									return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
								}
							}
						}
					},
				    series: [{
						type: 'pie',
						name: 'Browser share',
						data: eval("[{'name':'论文','y':33.8},{'name':'学者','y':6.4},{'name':'网页','y':6.9},{'name':'微博','y':44.2},{'name':'博客','y':6.7},{'name':'专利','y':2.0}]")
						
						
					}]
				});
			});