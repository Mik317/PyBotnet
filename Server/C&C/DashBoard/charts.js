function os(win,unix,mac){
var ctx = document.getElementById("Os");
			var myChart = new Chart(ctx, {
			    type: 'doughnut',
			    data: {
			        labels: ["Win", "Nix", "Mac"],
			        datasets: [{
			            label: 'Os',
			            data: [win,unix,mac],
			            backgroundColor: [
			                'rgba(255, 99, 132, 0.7)',
			                'rgba(54, 162, 235, 0.7)',
			                'rgba(255, 206, 86, 0.7)'
			            ],
			            borderColor: [
			                'rgba(255,99,132,1)',
			                'rgba(54, 162, 235, 1)',
			                'rgba(255, 206, 86, 1)'
			            ]}]},
			            options:{responsive: true}});
}
	
function os2(win,unix,mac){
			var ctx2 = document.getElementById("Os2");
			var myChart = new Chart(ctx2, {
			    type: 'bar',
			    data: {
			        labels: ["Win","Unix","Mac"],
			        datasets: [{
			            label: 'Bots\' Os',
			            data: [win,unix,mac],
			            backgroundColor: [
			                'rgba(255, 99, 132, 0.7)',
			                'rgba(54, 162, 235, 0.7)',
			                'rgba(255, 206, 86, 0.7)'
			            ],
			            borderColor: [
			                'rgba(255,99,132,1)',
			                'rgba(54, 162, 235, 1)',
			                'rgba(255, 206, 86, 1)'
			            ]}]},
			            options:{responsive: true}});
}

function total(num){
	var ctx3 = document.getElementById("AllBots");
	var myChart = new Chart(ctx3, {
	    type: 'polarArea',
	    data: {
	        labels: ["Bots"],
	        datasets: [{
	            label: 'Total Bots',
	            data: [num],
	            backgroundColor: [
	                'rgba(54, 162, 235, 0.7)',
	            ],
	            borderColor: [
	                'rgba(54, 162, 235, 1)',
	            ]}]},
	            options:{responsive: true}});
}
