

		var bkgroundColor = 'rgba(10, 70, 192, 0.1)';

		var data_mse = {
			datasets: [
			{
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 3,
				data: mse_json['data'],
				//hidden: true,
				//label: mse_json['conf']
			}
			]
		};

		var options_mse = {
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
					type: 'linear',
					stacked: false,
					ticks: {
					},
					scaleLabel: {
        				display: true,
        				labelString: 'log(mse)',
      			}
				}],
				xAxes: [{
					type: 'logarithmic',
					ticks: {
					},
					scaleLabel: {
        				display: true,
        				labelString: 'threshold',
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

function drawMSEChart(){
		var chart = new Chart(ctx_mse, {
			type: 'line',
			data: data_mse,
			options: options_mse,
		});
}

$('[href=\\#mse-threshold]').on('shown.bs.tab', function(event){
	drawMSEChart();
});		
		
