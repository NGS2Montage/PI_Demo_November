

		var bkgroundColor = 'rgba(10, 70, 192, 0.1)';

		var data = {
			datasets: [
			{
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[0]['data'],
				//hidden: true,
				label: contour_json[0]['conf']
			}, {
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[1]['data'],
				//hidden: true,
				label: contour_json[1]['conf']
			}, {
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[2]['data'],
				//hidden: true,
				label: contour_json[2]['conf']
			},{
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[3]['data'],
				//hidden: true,
				label: contour_json[3]['conf']
			},			{
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[4]['data'],
				//hidden: true,
				label: contour_json[4]['conf']
			}, {
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[5]['data'],
				//hidden: true,
				label: contour_json[5]['conf']
			},	{
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: contour_json[6]['data'],
				//hidden: true,
				label: contour_json[6]['conf']
			},
			]
		};

		var options = {
			annotation: {
				annotations: [
					{
						type: "line",
						mode: "vertical",
						scaleID: "x-axis-0",
						value: xi,
						borderColor: "red",
						label: {
							content: "Current Error",
							enabled: true,
							position: "top",						
						}				
					}				
				]
			},
			maintainAspectRatio: false,
			spanGaps: false,
			elements: {
				line: {
					tension: 0.000001,
					borderWidth: 0,
				},
				point: {
					radius: 0,				
				},
			},
			legend:{
				display: false,
			},
			scales: {
				yAxes: [{
					ticks: {
					min: 0,
					max: 1,
					},
					stacked: false,
					scaleLabel: {
        				display: true,
        				labelString: 'correct prediction ratio (individual error / total)',
      			}
				}],
				xAxes: [{
					type: 'logarithmic',
					ticks: {
					min: 0.05,
					max: 256,
					},
					scaleLabel: {
        				display: true,
        				labelString: 'dimensionless error',
      			}
				}],
			},
			plugins: {
				filler: {
					propagate: false
				},
				samples_filler_analyser: {
					target: 'chart-analyser'
				}
			}
		};

function drawContourChart(){
		var chart = new Chart(ctx, {
			type: 'line',
			data: data,
			options: options
		});
}

drawContourChart();

$('[href=\\#chart]').on('shown.bs.tab', function(event){
	drawContourChart();
});		
		
