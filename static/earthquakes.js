var map, data;
var ZOOM_THRESH = 5;

function initialize() {
	var mapOptions = {
		zoom: 2,
		center: new google.maps.LatLng(0, 0),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};

	map = new google.maps.Map(document.getElementById('map-canvas'),
		mapOptions);

	var zoomLevel = map.getZoom();
	if(zoomLevel < ZOOM_THRESH) {
		setHeatMap(earthquakes);
	} else {
		plotPoints(earthquakes);
	}

	google.maps.event.addListener(map, 'zoom_changed', function() {
		var oldZoomLevel = zoomLevel;
		zoomLevel = map.getZoom();

		if(oldZoomLevel < ZOOM_THRESH && zoomLevel >= ZOOM_THRESH) {
			plotPoints(earthquakes);
		}

		if(oldZoomLevel >= ZOOM_THRESH && zoomLevel < ZOOM_THRESH) {
			setHeatMap(earthquakes);
		}
  });

  google.maps.event.addListener(map, 'idle', sendMapBounds);

  function sendMapBounds() {
  	var request = new XMLHttpRequest();
		request.open("get", "/" + "?bounds=" + map.getBounds());
		request.send();
  }

	function plotPoints(earthquakes) {
		earthquakes.forEach(function(eq) {
			var latitude = eq[2];
			var longitude = eq[3];
			var latLng = new google.maps.LatLng(latitude, longitude);

			var eventName = eq[1];
			var icon = {
				url: '/static/beachballs/' + eventName + '.png',
				scaledSize: new google.maps.Size(30, 30) 
			};

	    var marker = new google.maps.Marker({
	      position: latLng,
	      map: map,
	      icon: icon
	    });
		})
	}

	function setHeatMap(earthquakes) {
		var heatmapData = [];
		earthquakes.forEach(function(eq) {
			var latitude = eq[2];
			var longitude = eq[3];
			var latLng = new google.maps.LatLng(latitude, longitude);
			heatmapData.push(latLng);
		})

  	var heatmap = new google.maps.visualization.HeatmapLayer({
    	data: heatmapData
  	});

  	heatmap.setMap(map);
	}
}

google.maps.event.addDomListener(window, 'load', initialize);