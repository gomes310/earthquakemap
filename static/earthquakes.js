var map, data, heatmapData, heatmap;

function initialize() {
	var mapOptions = {
		zoom: 2,
		center: new google.maps.LatLng(0, 0),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};

	map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);

	heatmapData = [];
	plotPoints(earthquakes);

	function plotPoints(earthquakes) {
		earthquakes.forEach(function(eq) {
			var latitude = eq[2];
			var longitude = eq[3];
			var latLng = new google.maps.LatLng(latitude, longitude);
			heatmapData.push(latLng);
			var eventName = eq[1];
			// var icon = {
			// 	url: '/static/' + eventName + '.png',
			// 	scaledSize: new google.maps.Size(20, 20) 
			// };

	  //   var marker = new google.maps.Marker({
	  //     position: latLng,
	  //     map: map,
	  //     icon: icon
	  //   });
		})
	}

	function setHeatMap() {
		var pointArray = new google.maps.MVCArray(heatmapData);
  	heatmap = new google.maps.visualization.HeatmapLayer({
    	data: pointArray
  	});

  	heatmap.setMap(map);
	}
}

google.maps.event.addDomListener(window, 'load', initialize);