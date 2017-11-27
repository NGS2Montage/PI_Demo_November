

		var bkgroundColor = 'rgba(10, 70, 192, 0.1)';

		var data_error = {
			datasets: [
			{
				backgroundColor: bkgroundColor,
				borderColor: 'black',
				borderWidth: 1,
				data: error_json['data'],
				//hidden: true,
				label: error_json['xi']
			}
			]
		};

		var options_error = {
			annotation: {
				annotations: [
					{
						type: "line",
						
						mode: "vertical",
						scaleID: "x-axis-0",
						value: nErr,
						borderColor: "red",
						label: {
							content: "Ind. Error Level",
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
					stacked: false,
					scaleLabel: {
        				display: true,
        				labelString: 'error pdf',
      			}
				}],
				xAxes: [{
					type: 'linear',
					ticks: {
					min: 0,
					max: nObs,
					},
				scaleLabel: {
        				display: true,
        				labelString: 'Individual Error Count',
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

function drawErrorChart(){
		var chart_error = new Chart(ctx_error, {
			type: 'line',
			data: data_error,
			options: options_error,
		});
	}
	
$('[href=\\#zoom]').on('shown.bs.tab', function(event){
	drawErrorChart();
});
	